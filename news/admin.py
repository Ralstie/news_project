# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Article, Newsletter, Publisher, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):    

    fieldsets = UserAdmin.fieldsets + (
        ("News Application", {"fields": ("role",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("News Application", {"fields": ("role",)}),
    )

    list_display = (
        "username",
        "email",
        "role",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "role",
        "is_staff",
        "is_active",
    )


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):    

    list_display = (
        "name",
        "website",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
    )

    filter_horizontal = (
        "editors",
        "journalists",
    )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):    

    list_display = (
        "title",
        "author",
        "publisher",
        "approved",
        "created_at",
    )

    list_filter = (
        "approved",
        "publisher",
        "created_at",
    )

    search_fields = (
        "title",
        "content",
        "author__username",
    )


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):    

    list_display = (
        "title",
        "author",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "author__username",
    )

    filter_horizontal = (
        "articles",
    )
