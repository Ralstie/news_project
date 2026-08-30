from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        READER = "READER", "Reader"
        EDITOR = "EDITOR", "Editor"
        JOURNALIST = "JOURNALIST", "Journalist"
        PUBLISHER = "PUBLISHER", "Publisher"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.READER,
    )


class Publisher(models.Model):

    name = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    website = models.URLField(blank=True)

    publishers = models.ManyToManyField(
        "User",
        related_name="publisher_accounts",
        blank=True,
        limit_choices_to={"role": "PUBLISHER"},
    )

    editors = models.ManyToManyField(
        "User",
        related_name="editor_publishers",
        blank=True,
        limit_choices_to={"role": "EDITOR"},
    )

    journalists = models.ManyToManyField(
        "User",
        related_name="journalist_publishers",
        blank=True,
        limit_choices_to={"role": "JOURNALIST"},
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Article(models.Model):

    title = models.CharField(max_length=255)
    content = models.TextField()

    author = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="articles",
        limit_choices_to={"role": User.Role.JOURNALIST},
    )

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
    )

    approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("approve_article", "Can approve article"),
        ]

    def __str__(self):
        return self.title

    def clean(self):
        if self.author.role != User.Role.JOURNALIST:
            raise ValidationError(
                "Only journalists can be article authors."
            )

        if self.publisher is None:
            return

        journalist_ids = self.publisher.journalists.values_list(
            "id",
            flat=True,
        )

        if self.author_id not in journalist_ids:
            raise ValidationError(
                "This journalist is not assigned to the selected publisher."
            )

class Newsletter(models.Model):
    
    title = models.CharField(max_length=255)
    description = models.TextField()

    author = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="newsletters",
        limit_choices_to={"role": User.Role.JOURNALIST},
    )

    articles = models.ManyToManyField(
        Article,
        related_name="newsletters",
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def clean(self):
        
        from django.core.exceptions import ValidationError

        if self.author.role != User.Role.JOURNALIST:
            raise ValidationError(
                "Only journalists can be newsletter authors."
            )
    