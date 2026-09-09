"""Database models for the NewsHub application.

This module defines users, publishers, articles, and newsletters,
including their relationships and validation rules.
"""

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    """Custom user model with role-based access to the news application."""

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

    subscribed_publishers = models.ManyToManyField(
        "Publisher",
        related_name="subscribers",
        blank=True,
    )

    subscribed_journalists = models.ManyToManyField(
        "self",
        related_name="journalist_subscribers",
        symmetrical=False,
        blank=True,
        limit_choices_to={"role": "JOURNALIST"},
    )


class Publisher(models.Model):
    """Represents a news publisher and its assigned staff."""

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)

    publishers = models.ManyToManyField(
        "User",
        related_name="publisher_accounts",
        blank=True,
        limit_choices_to={"role": User.Role.PUBLISHER},
    )

    editors = models.ManyToManyField(
        "User",
        related_name="editor_publishers",
        blank=True,
        limit_choices_to={"role": User.Role.EDITOR},
    )

    journalists = models.ManyToManyField(
        "User",
        related_name="journalist_publishers",
        blank=True,
        limit_choices_to={"role": User.Role.JOURNALIST},
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    """A news article written by a journalist."""

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
        """Ensure articles are written by assigned journalists."""

        if self.author.role != User.Role.JOURNALIST:
            raise ValidationError("Only journalists can be article authors.")

        if self.publisher is None:
            return

        if not self.publisher.journalists.filter(
            id=self.author_id
        ).exists():
            raise ValidationError(
                "This journalist is not assigned to the selected publisher."
            )


class Newsletter(models.Model):
    """A newsletter assembled by a journalist from approved articles."""

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
        """Ensure newsletters are created by journalists."""

        if self.author.role != User.Role.JOURNALIST:
            raise ValidationError(
                "Only journalists can be newsletter authors."
            )
