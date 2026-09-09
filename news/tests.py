from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from .models import Article, Publisher

User = get_user_model()


@override_settings(
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }
)
class ArticleAPITests(TestCase):
    """Verify article REST API CRUD operations and access control."""

    def setUp(self):
        self.client = APIClient()
        self.journalist = User.objects.create_user(
            username="journalist",
            password="testpass123",
            role=User.Role.JOURNALIST,
        )
        self.other_journalist = User.objects.create_user(
            username="other",
            password="testpass123",
            role=User.Role.JOURNALIST,
        )
        self.reader = User.objects.create_user(
            username="reader",
            password="testpass123",
            role=User.Role.READER,
        )
        self.article = Article.objects.create(
            title="Approved article",
            content="Article content.",
            author=self.journalist,
            approved=True,
        )

    def test_list_articles(self):
        response = self.client.get("/api/articles/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Approved article")

    def test_reader_cannot_create_article(self):
        self.client.force_authenticate(user=self.reader)
        response = self.client.post(
            "/api/articles/",
            {"title": "New", "content": "Content"},
        )
        self.assertEqual(response.status_code, 403)

    def test_journalist_can_create_article(self):
        self.client.force_authenticate(user=self.journalist)
        response = self.client.post(
            "/api/articles/",
            {"title": "New", "content": "Content"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["author"], self.journalist.id)
        self.assertFalse(response.data["approved"])

    def test_journalist_can_update_own_article(self):
        self.client.force_authenticate(user=self.journalist)
        response = self.client.patch(
            f"/api/articles/{self.article.id}/",
            {"title": "Updated title"},
        )
        self.assertEqual(response.status_code, 200)
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, "Updated title")

    def test_journalist_can_delete_own_article(self):
        self.client.force_authenticate(user=self.journalist)
        response = self.client.delete(
            f"/api/articles/{self.article.id}/"
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            Article.objects.filter(id=self.article.id).exists()
        )

    def test_journalist_cannot_update_another_journalists_article(self):
        self.client.force_authenticate(user=self.other_journalist)
        response = self.client.patch(
            f"/api/articles/{self.article.id}/",
            {"title": "Not allowed"},
        )
        self.assertEqual(response.status_code, 403)

    def test_retrieve_article(self):
        response = self.client.get(
            f"/api/articles/{self.article.id}/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.article.id)


@override_settings(
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }
)
class NewsWorkflowAPITests(TestCase):
    """Verify the approval log and subscribed-articles API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.reader = User.objects.create_user(
            username="reader2",
            password="testpass123",
            role=User.Role.READER,
        )
        self.journalist = User.objects.create_user(
            username="journalist2",
            password="testpass123",
            role=User.Role.JOURNALIST,
        )
        self.other_journalist = User.objects.create_user(
            username="journalist3",
            password="testpass123",
            role=User.Role.JOURNALIST,
        )
        self.publisher = Publisher.objects.create(name="Subscribed Publisher")
        self.reader.subscribed_journalists.add(self.journalist)
        self.reader.subscribed_publishers.add(self.publisher)

        self.subscribed_journalist_article = Article.objects.create(
            title="Journalist article",
            content="Content",
            author=self.journalist,
            approved=True,
        )
        self.subscribed_publisher_article = Article.objects.create(
            title="Publisher article",
            content="Content",
            author=self.other_journalist,
            publisher=self.publisher,
            approved=True,
        )
        Article.objects.create(
            title="Unapproved article",
            content="Content",
            author=self.journalist,
            publisher=self.publisher,
            approved=False,
        )
        Article.objects.create(
            title="Unsubscribed article",
            content="Content",
            author=self.other_journalist,
            approved=True,
        )

    def test_approved_article_log_api_accepts_post(self):
        response = self.client.post(
            "/api/approved/",
            {
                "article_id": self.subscribed_journalist_article.id,
                "title": self.subscribed_journalist_article.title,
                "approved": True,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data["article"]["article_id"],
            self.subscribed_journalist_article.id,
        )

    def test_subscribed_articles_returns_journalist_and_publisher_articles(self):
        self.client.force_authenticate(user=self.reader)
        response = self.client.get("/api/articles/subscribed/")

        self.assertEqual(response.status_code, 200)
        titles = {article["title"] for article in response.data}
        self.assertEqual(
            titles,
            {"Journalist article", "Publisher article"},
        )

    def test_subscribed_articles_requires_reader_role(self):
        self.client.force_authenticate(user=self.journalist)
        response = self.client.get("/api/articles/subscribed/")
        self.assertEqual(response.status_code, 403)
