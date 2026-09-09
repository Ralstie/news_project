"""Serializers for the NewsHub REST API."""

from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """Serialize articles for the REST API."""

    author = serializers.PrimaryKeyRelatedField(read_only=True)
    approved = serializers.BooleanField(read_only=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "author",
            "publisher",
            "approved",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "author",
            "approved",
            "created_at",
            "updated_at",
        ]
