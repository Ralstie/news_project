from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ArticleForm, NewsletterForm, RegistrationForm
from .models import Article, Newsletter, Publisher, User
from django.core.mail import send_mail

def home(request):    

    articles = Article.objects.filter(
        approved=True
    ).select_related(
        "author",
        "publisher",
    ).order_by("-created_at")

    newsletters = Newsletter.objects.all().order_by(
        "-created_at"
    )[:6]

    return render(
        request,
        "news/home.html",
        {
            "articles": articles,
            "newsletters": newsletters,
        },
    )


def register(request):    

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

    return render(
        request,
        "news/register.html",
        {"form": form},
    )


@login_required
def article_list(request):
    articles = Article.objects.filter(
        approved=True
    ).order_by("-created_at")

    return render(
        request,
        "news/article_list.html",
        {"articles": articles},
    )


def article_detail(request, article_id):
    
    article = get_object_or_404(
        Article.objects.select_related(
            "author",
            "publisher",
        ),
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

    newsletters = Newsletter.objects.all().order_by(
        "-created_at"
    )

    return render(
        request,
        "news/newsletter_list.html",
        {"newsletters": newsletters},
    )


@login_required
def newsletter_detail(request, newsletter_id):    

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

    publishers = Publisher.objects.all().order_by("name")

    return render(
        request,
        "news/publisher_list.html",
        {"publishers": publishers},
    )


@login_required
def publisher_detail(request, publisher_id):    

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
def journalist_dashboard(request):
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

    context = {
        "articles": articles,
        "newsletters": newsletters,
    }

    return render(
        request,
        "news/journalist_dashboard.html",
        context,
    )


@login_required
def article_create(request):
    if request.user.role != "JOURNALIST":
        messages.error(
            request,
            "Only journalists can create articles.",
        )
        return redirect("home")

    if request.method == "POST":
        article = Article(author=request.user)

        form = ArticleForm(
            request.POST,
            instance=article,
        )

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
        form = ArticleForm()

    return render(
        request,
        "news/article_form.html",
        {"form": form},
    )


@login_required
def article_edit(request, article_id):    

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

            # Editing an article sends it back for approval.
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

    article = get_object_or_404(
        Article,
        id=article_id,
    )
    
    if request.user.role != User.Role.JOURNALIST:
        return HttpResponseForbidden("You are not allowed to delete articles.")

    
    if article.author != request.user:
        return HttpResponseForbidden(
            "You are not allowed to delete this article."
        )
    
    if article.approved:
        return HttpResponseForbidden(
            "Approved articles cannot be deleted."
        )

    if request.method == "POST":
        article.delete()

        messages.success(
            request,
            "Article deleted successfully."
        )

        return redirect("journalist_dashboard")

    return render(
        request,
        "news/article_confirm_delete.html",
        {
            "article": article,
        },
    )


@login_required
def newsletter_create(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        
        form.instance.author = request.user

        if form.is_valid():
            newsletter = form.save()

            return redirect("journalist_dashboard")
    else:
        form = NewsletterForm()
        
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
    newsletter = get_object_or_404(
        Newsletter,
        pk=pk,
        author=request.user,
    )

    if request.method == "POST":
        newsletter.delete()
        return redirect("journalist_dashboard")

    return render(
        request,
        "news/newsletter_confirm_delete.html",
        {"newsletter": newsletter},
    )


@login_required
def editor_dashboard(request):
    if request.user.role != User.Role.EDITOR:
        return redirect("home")

    pending_articles = Article.objects.filter(
        approved=False
    ).order_by("-created_at")

    return render(
        request,
        "news/editor_dashboard.html",
        {
            "pending_articles": pending_articles,
        },
    )


@login_required
def approve_article(request, article_id):
    if request.method != "POST":
        return redirect("editor_dashboard")

    if request.user.role != "EDITOR":
        return redirect("home")

    article = get_object_or_404(
        Article,
        id=article_id,
    )

    article.approved = True
    article.save()

    send_mail(
        subject=f"New article approved: {article.title}",
        message=(
            f"A new article has been approved.\n\n"
            f"Title: {article.title}\n"
            f"Author: {article.author.username}\n\n"
            f"{article.content}"
        ),
        from_email=None,
        recipient_list=[
            article.author.email,
        ],
        fail_silently=False,
    )

    messages.success(
        request,
        "Article approved successfully.",
    )

    return redirect("editor_dashboard")

@login_required
def publisher_dashboard(request):

    if request.user.role != User.Role.PUBLISHER:
        return redirect("home")

    publishers = Publisher.objects.filter(
        publishers=request.user
    )

    articles = Article.objects.filter(
        publisher__in=publishers
    ).order_by("-created_at")

    newsletters = Newsletter.objects.filter(
        articles__publisher__in=publishers
    ).distinct().order_by("-created_at")

    context = {
        "publishers": publishers,
        "articles": articles,
        "newsletters": newsletters,
    }

    return render(
        request,
        "news/publisher_dashboard.html",
        context,
    )