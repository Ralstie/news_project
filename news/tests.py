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
