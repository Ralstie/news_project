from django.contrib import messages
from django.contrib.auth import login
from django.db import models
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ArticleForm, NewsletterForm, PublisherForm, RegistrationForm
from .models import Article, Newsletter, Publisher, User
from .permissions import IsJournalistOrReadOnly
from .serializers import ArticleSerializer

import logging
import requests


logger = logging.getLogger(__name__)


def home(request):
    """Display approved articles and the latest newsletters."""
    articles = Article.objects.filter(
        approved=True
    ).select_related(
        "author",
        "publisher",
    ).order_by("-created_at")

    newsletters = Newsletter.objects.all().order_by("-created_at")[:6]

    return render(
        request,
        "news/home.html",
        {"articles": articles, "newsletters": newsletters},
    )


def register(request):
    """Register a user and sign them in."""
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                "Your account has been created successfully.",
            )
            return redirect("home")
    else:
        form = RegistrationForm()

    return render(request, "news/register.html", {"form": form})


@login_required
def article_list(request):
    """List approved articles."""
    articles = Article.objects.filter(
        approved=True
    ).select_related(
        "author",
        "publisher",
    ).order_by("-created_at")

    return render(
        request,
        "news/article_list.html",
        {"articles": articles},
    )


def article_detail(request, article_id):
    """Display one approved article."""
    article = get_object_or_404(
        Article.objects.select_related("author", "publisher"),
        id=article_id,
        approved=True,
    )

    return render(
        request,
        "news/article_detail.html",
        {"article": article},
    )


@login_required
def newsletter_list(request):
    """List newsletters."""
    newsletters = Newsletter.objects.all().order_by("-created_at")

    return render(
        request,
        "news/newsletter_list.html",
        {"newsletters": newsletters},
    )


@login_required
def newsletter_detail(request, newsletter_id):
    """Display a newsletter and its approved articles."""
    newsletter = get_object_or_404(
        Newsletter,
        id=newsletter_id,
    )

    articles = newsletter.articles.filter(
        approved=True
    ).select_related(
        "author",
        "publisher",
    )

    return render(
        request,
        "news/newsletter_detail.html",
        {
            "newsletter": newsletter,
            "articles": articles,
        },
    )


@login_required
def publisher_list(request):
    """Display all publishers."""
    publishers = Publisher.objects.all().order_by("name")

    return render(
        request,
        "news/publisher_list.html",
        {"publishers": publishers},
    )


@login_required
def publisher_detail(request, publisher_id):
    """Display a publisher and its approved articles."""
    publisher = get_object_or_404(
        Publisher,
        id=publisher_id,
    )

    articles = publisher.articles.filter(
        approved=True
    ).select_related("author")

    return render(
        request,
        "news/publisher_detail.html",
        {
            "publisher": publisher,
            "articles": articles,
        },
    )


@login_required
def publisher_create(request):
    """Allow a publisher account to create a publisher profile."""
    if request.user.role != User.Role.PUBLISHER:
        raise PermissionDenied

    if request.method == "POST":
        form = PublisherForm(request.POST)

        if form.is_valid():
            publisher = form.save()
            publisher.publishers.add(request.user)

            messages.success(
                request,
                "Publisher created successfully.",
            )

            return redirect("publisher_dashboard")
    else:
        form = PublisherForm()

    return render(
        request,
        "news/publisher_form.html",
        {
            "form": form,
            "page_title": "Create Publisher",
        },
    )


@login_required
def publisher_edit(request, publisher_id):
    """Allow a publisher owner to update its profile and staff."""
    if request.user.role != User.Role.PUBLISHER:
        raise PermissionDenied

    publisher = get_object_or_404(
        Publisher,
        id=publisher_id,
        publishers=request.user,
    )

    if request.method == "POST":
        form = PublisherForm(
            request.POST,
            instance=publisher,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Publisher updated successfully.",
            )

            return redirect("publisher_dashboard")
    else:
        form = PublisherForm(instance=publisher)

    return render(
        request,
        "news/publisher_form.html",
        {
            "form": form,
            "page_title": "Edit Publisher",
        },
    )


@login_required
def publisher_delete(request, publisher_id):
    """Allow a publisher owner to delete its publisher profile."""
    if request.user.role != User.Role.PUBLISHER:
        raise PermissionDenied

    publisher = get_object_or_404(
        Publisher,
        id=publisher_id,
        publishers=request.user,
    )

    if request.method == "POST":
        publisher.delete()

        messages.success(
            request,
            "Publisher deleted successfully.",
        )

        return redirect("publisher_dashboard")

    return render(
        request,
        "news/publisher_confirm_delete.html",
        {"publisher": publisher},
    )


@login_required
def journalist_dashboard(request):
    """Display content owned by the logged-in journalist."""
    if request.user.role != User.Role.JOURNALIST:
        messages.error(
            request,
            "Only journalists can access the journalist dashboard.",
        )

        return redirect("home")

    articles = Article.objects.filter(
        author=request.user
    ).order_by("-created_at")

    newsletters = Newsletter.objects.filter(
        author=request.user
    ).order_by("-created_at")

    return render(
        request,
        "news/journalist_dashboard.html",
        {
            "articles": articles,
            "newsletters": newsletters,
        },
    )


@login_required
def article_create(request):
    """Allow a journalist to submit an article for approval."""
    if request.user.role != User.Role.JOURNALIST:
        messages.error(
            request,
            "Only journalists can create articles.",
        )

        return redirect("home")

    if request.method == "POST":
        form = ArticleForm(
            request.POST,
            user=request.user,
        )

        # IMPORTANT:
        # Set the author BEFORE form.is_valid().
        # Article.clean() accesses self.author.role during validation.
        form.instance.author = request.user

        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.approved = False
            article.save()

            messages.success(
                request,
                "Article submitted successfully and is waiting for editor approval.",
            )

            return redirect("journalist_dashboard")
    else:
        form = ArticleForm(user=request.user)

        # Also set the author on the form instance for consistency.
        form.instance.author = request.user

    return render(
        request,
        "news/article_form.html",
        {
            "form": form,
            "page_title": "Create Article",
        },
    )


@login_required
def article_edit(request, article_id):
    """Allow a journalist to edit their own article."""
    if request.user.role != User.Role.JOURNALIST:
        raise PermissionDenied

    article = get_object_or_404(
        Article,
        id=article_id,
        author=request.user,
    )

    if request.method == "POST":
        form = ArticleForm(
            request.POST,
            instance=article,
            user=request.user,
        )

        if form.is_valid():
            article = form.save(commit=False)
            article.approved = False
            article.save()

            messages.success(
                request,
                "Article updated and returned for approval.",
            )

            return redirect("journalist_dashboard")
    else:
        form = ArticleForm(
            instance=article,
            user=request.user,
        )

    return render(
        request,
        "news/article_form.html",
        {
            "form": form,
            "page_title": "Edit Article",
        },
    )


@login_required
def article_delete(request, article_id):
    """Allow a journalist to delete their own unapproved article."""
    article = get_object_or_404(
        Article,
        id=article_id,
    )

    if request.user.role != User.Role.JOURNALIST:
        return HttpResponseForbidden(
            "You are not allowed to delete articles."
        )

    if article.author != request.user:
        return HttpResponseForbidden(
            "You are not allowed to delete this article."
        )

    if article.approved:
        return HttpResponseForbidden(
            "Approved articles cannot be deleted by journalists."
        )

    if request.method == "POST":
        article.delete()

        messages.success(
            request,
            "Article deleted successfully.",
        )

        return redirect("journalist_dashboard")

    return render(
        request,
        "news/article_confirm_delete.html",
        {"article": article},
    )


@login_required
def newsletter_create(request):
    """Allow a journalist to create a newsletter."""
    if request.user.role != User.Role.JOURNALIST:
        raise PermissionDenied

    if request.method == "POST":
        form = NewsletterForm(
            request.POST,
            user=request.user,
        )

        # Set the author before form/model validation.
        form.instance.author = request.user

        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.author = request.user
            newsletter.save()
            form.save_m2m()

            messages.success(
                request,
                "Newsletter created successfully.",
            )

            return redirect("journalist_dashboard")
    else:
        form = NewsletterForm(user=request.user)
        form.instance.author = request.user

    return render(
        request,
        "news/newsletter_form.html",
        {
            "form": form,
            "page_title": "Create Newsletter",
        },
    )


@login_required
def newsletter_edit(request, newsletter_id):
    """Allow a journalist to edit their own newsletter."""
    if request.user.role != User.Role.JOURNALIST:
        raise PermissionDenied

    newsletter = get_object_or_404(
        Newsletter,
        id=newsletter_id,
        author=request.user,
    )

    if request.method == "POST":
        form = NewsletterForm(
            request.POST,
            instance=newsletter,
            user=request.user,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Newsletter updated successfully.",
            )

            return redirect("journalist_dashboard")
    else:
        form = NewsletterForm(
            instance=newsletter,
            user=request.user,
        )

    return render(
        request,
        "news/newsletter_form.html",
        {
            "form": form,
            "page_title": "Edit Newsletter",
        },
    )


@login_required
def newsletter_delete(request, pk):
    """Allow a journalist to delete their own newsletter."""
    newsletter = get_object_or_404(
        Newsletter,
        pk=pk,
        author=request.user,
    )

    if request.user.role != User.Role.JOURNALIST:
        raise PermissionDenied

    if request.method == "POST":
        newsletter.delete()

        messages.success(
            request,
            "Newsletter deleted successfully.",
        )

        return redirect("journalist_dashboard")

    return render(
        request,
        "news/newsletter_confirm_delete.html",
        {"newsletter": newsletter},
    )


@login_required
def editor_dashboard(request):
    """Give editors access to all article and newsletter management."""
    if request.user.role != User.Role.EDITOR:
        return redirect("home")

    articles = Article.objects.select_related(
        "author",
        "publisher",
    ).order_by("-created_at")

    newsletters = Newsletter.objects.select_related(
        "author"
    ).prefetch_related(
        "articles"
    ).order_by("-created_at")

    return render(
        request,
        "news/editor_dashboard.html",
        {
            "articles": articles,
            "newsletters": newsletters,
            "pending_articles": articles.filter(approved=False),
        },
    )


@login_required
def editor_article_detail(request, article_id):
    """Allow an editor to view an article, including pending articles."""
    if request.user.role != User.Role.EDITOR:
        raise PermissionDenied

    article = get_object_or_404(
        Article.objects.select_related(
            "author",
            "publisher",
        ),
        id=article_id,
    )

    return render(
        request,
        "news/editor_article_detail.html",
        {"article": article},
    )


@login_required
def editor_article_edit(request, article_id):
    """Allow an editor to update any article."""
    if request.user.role != User.Role.EDITOR:
        raise PermissionDenied

    article = get_object_or_404(
        Article,
        id=article_id,
    )

    if request.method == "POST":
        form = ArticleForm(
            request.POST,
            instance=article,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Article updated successfully.",
            )

            return redirect("editor_dashboard")
    else:
        form = ArticleForm(instance=article)

    return render(
        request,
        "news/article_form.html",
        {
            "form": form,
            "page_title": "Edit Article",
        },
    )


@login_required
def editor_article_delete(request, article_id):
    """Allow an editor to delete any article."""
    if request.user.role != User.Role.EDITOR:
        raise PermissionDenied

    article = get_object_or_404(
        Article,
        id=article_id,
    )

    if request.method == "POST":
        article.delete()

        messages.success(
            request,
            "Article deleted successfully.",
        )

        return redirect("editor_dashboard")

    return render(
        request,
        "news/article_confirm_delete.html",
        {"article": article},
    )


@login_required
def editor_newsletter_edit(request, newsletter_id):
    """Allow an editor to update any newsletter."""
    if request.user.role != User.Role.EDITOR:
        raise PermissionDenied

    newsletter = get_object_or_404(
        Newsletter,
        id=newsletter_id,
    )

    if request.method == "POST":
        form = NewsletterForm(
            request.POST,
            instance=newsletter,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Newsletter updated successfully.",
            )

            return redirect("editor_dashboard")
    else:
        form = NewsletterForm(instance=newsletter)

    return render(
        request,
        "news/newsletter_form.html",
        {
            "form": form,
            "page_title": "Edit Newsletter",
        },
    )


@login_required
def editor_newsletter_delete(request, newsletter_id):
    """Allow an editor to delete any newsletter."""
    if request.user.role != User.Role.EDITOR:
        raise PermissionDenied

    newsletter = get_object_or_404(
        Newsletter,
        id=newsletter_id,
    )

    if request.method == "POST":
        newsletter.delete()

        messages.success(
            request,
            "Newsletter deleted successfully.",
        )

        return redirect("editor_dashboard")

    return render(
        request,
        "news/newsletter_confirm_delete.html",
        {"newsletter": newsletter},
    )


@login_required
def approve_article(request, article_id):
    """Approve an article, notify all relevant subscribers and log the approval."""
    if request.method != "POST" or request.user.role != User.Role.EDITOR:
        return redirect("home")

    article = get_object_or_404(
        Article.objects.select_related(
            "author",
            "publisher",
        ),
        id=article_id,
    )

    article.approved = True
    article.save(
        update_fields=[
            "approved",
            "updated_at",
        ]
    )

    recipients = set()

    if article.author.email:
        recipients.add(article.author.email)

    journalist_subscribers = User.objects.filter(
        subscribed_journalists=article.author,
        email__isnull=False,
    ).exclude(
        email=""
    ).values_list(
        "email",
        flat=True,
    )

    recipients.update(journalist_subscribers)

    if article.publisher_id:
        publisher_subscribers = User.objects.filter(
            subscribed_publishers=article.publisher,
            email__isnull=False,
        ).exclude(
            email=""
        ).values_list(
            "email",
            flat=True,
        )

        recipients.update(publisher_subscribers)

    if recipients:
        send_mail(
            subject=f"New article approved: {article.title}",
            message=(
                f"A new article has been approved.\n\n"
                f"Title: {article.title}\n"
                f"Author: {article.author.username}\n\n"
                f"{article.content}"
            ),
            from_email=None,
            recipient_list=sorted(recipients),
            fail_silently=False,
        )

    payload = {
        "article_id": article.id,
        "title": article.title,
        "content": article.content,
        "author_id": article.author_id,
        "publisher_id": article.publisher_id,
        "approved": article.approved,
    }

    api_url = request.build_absolute_uri(
        reverse("approved-article-log-api")
    )

    try:
        response = requests.post(
            api_url,
            json=payload,
            timeout=5,
        )

        response.raise_for_status()

    except requests.RequestException as exc:
        logger.exception(
            "Failed to log approved article %s: %s",
            article.id,
            exc,
        )

        messages.error(
            request,
            "The article was approved, but the approval log could not be created.",
        )

        return redirect("editor_dashboard")

    messages.success(
        request,
        "Article approved successfully.",
    )

    return redirect("editor_dashboard")


class ApprovedArticleLogAPI(APIView):
    """Accept and log article approval data sent by the approval workflow."""

    permission_classes = [AllowAny]

    def post(self, request):
        article_data = request.data

        logger.info(
            "Approved article logged: %s",
            article_data,
        )

        return Response(
            {
                "message": "Approved article logged successfully.",
                "article": article_data,
            },
            status=status.HTTP_201_CREATED,
        )


class SubscribedArticlesAPI(APIView):
    """Return approved articles from a reader's subscriptions."""

    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
    ]

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != User.Role.READER:
            return Response(
                {
                    "detail": "Only readers can access subscribed articles."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        articles = Article.objects.filter(
            approved=True,
        ).filter(
            models.Q(
                author__in=request.user.subscribed_journalists.all()
            )
            |
            models.Q(
                publisher__in=request.user.subscribed_publishers.all()
            )
        ).select_related(
            "author",
            "publisher",
        ).distinct().order_by(
            "-created_at"
        )

        serializer = ArticleSerializer(
            articles,
            many=True,
        )

        return Response(serializer.data)


@login_required
def publisher_dashboard(request):
    """Display publisher profiles owned by the current publisher account."""
    if request.user.role != User.Role.PUBLISHER:
        return redirect("home")

    publishers = Publisher.objects.filter(
        publishers=request.user
    ).distinct()

    articles = Article.objects.filter(
        publisher__in=publishers
    ).order_by("-created_at")

    newsletters = Newsletter.objects.filter(
        articles__publisher__in=publishers
    ).distinct().order_by("-created_at")

    return render(
        request,
        "news/publisher_dashboard.html",
        {
            "publishers": publishers,
            "articles": articles,
            "newsletters": newsletters,
        },
    )


@login_required
def subscriptions(request):
    """Allow readers to subscribe and unsubscribe from publishers and journalists."""
    if request.user.role != User.Role.READER:
        raise PermissionDenied

    if request.method == "POST":
        item_type = request.POST.get("item_type")
        item_id = request.POST.get("item_id")

        if item_type == "publisher":
            publisher = get_object_or_404(
                Publisher,
                id=item_id,
            )

            relation = request.user.subscribed_publishers
            message = publisher.name

        elif item_type == "journalist":
            journalist = get_object_or_404(
                User,
                id=item_id,
                role=User.Role.JOURNALIST,
            )

            relation = request.user.subscribed_journalists
            message = journalist.username

        else:
            raise PermissionDenied

        if relation.filter(pk=item_id).exists():
            relation.remove(
                publisher if item_type == "publisher" else journalist
            )

            messages.success(
                request,
                f"Unsubscribed from {message}.",
            )
        else:
            relation.add(
                publisher if item_type == "publisher" else journalist
            )

            messages.success(
                request,
                f"Subscribed to {message}.",
            )

        return redirect("subscriptions")

    publishers = Publisher.objects.all().order_by("name")

    journalists = User.objects.filter(
        role=User.Role.JOURNALIST
    ).order_by("username")

    return render(
        request,
        "news/subscriptions.html",
        {
            "publishers": publishers,
            "journalists": journalists,
            "subscribed_publishers": request.user.subscribed_publishers.all(),
            "subscribed_journalists": request.user.subscribed_journalists.all(),
        },
    )


class ArticleListCreateAPI(APIView):
    """REST endpoint for listing and creating articles."""

    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
    ]

    permission_classes = [IsJournalistOrReadOnly]

    def get(self, request):
        """Return approved articles."""
        articles = Article.objects.filter(
            approved=True
        ).select_related(
            "author",
            "publisher",
        )

        serializer = ArticleSerializer(
            articles,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):
        """Create an article for the authenticated journalist."""
        serializer = ArticleSerializer(
            data=request.data
        )

        if serializer.is_valid():
            article = serializer.save(
                author=request.user
            )

            return Response(
                ArticleSerializer(article).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class ArticleDetailAPI(APIView):
    """REST endpoint for retrieving, updating and deleting an article."""

    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
    ]

    permission_classes = [IsJournalistOrReadOnly]

    def get_object(self, article_id):
        return get_object_or_404(
            Article,
            id=article_id,
        )

    def get(self, request, article_id):
        """Return one approved article."""
        article = self.get_object(article_id)

        if not article.approved:
            return Response(
                {"detail": "Article not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            ArticleSerializer(article).data
        )

    def put(self, request, article_id):
        """Replace an article owned by the authenticated journalist."""
        return self._update(
            request,
            article_id,
            partial=False,
        )

    def patch(self, request, article_id):
        """Partially update an article owned by the journalist."""
        return self._update(
            request,
            article_id,
            partial=True,
        )

    def _update(self, request, article_id, partial):
        article = self.get_object(article_id)

        if article.author != request.user:
            return Response(
                {
                    "detail": "You can only edit your own articles."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ArticleSerializer(
            article,
            data=request.data,
            partial=partial,
        )

        if serializer.is_valid():
            updated = serializer.save()

            return Response(
                ArticleSerializer(updated).data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, article_id):
        """Delete an article owned by the authenticated journalist."""
        article = self.get_object(article_id)

        if article.author != request.user:
            return Response(
                {
                    "detail": "You can only delete your own articles."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        article.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
