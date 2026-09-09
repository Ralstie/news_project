from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.db.models import Q


class Command(BaseCommand):
    """Create and configure the application's role groups."""

    help = "Create Reader, Editor, and Journalist groups and permissions."

    def handle(self, *args, **options):
        reader_group, _ = Group.objects.get_or_create(name="Reader")
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        journalist_group, _ = Group.objects.get_or_create(name="Journalist")

        reader_permissions = Permission.objects.filter(
            Q(
                content_type__app_label="news",
                content_type__model="article",
                codename="view_article",
            )
            | Q(
                content_type__app_label="news",
                content_type__model="newsletter",
                codename="view_newsletter",
            )
        )

        editor_permissions = Permission.objects.filter(
            Q(
                content_type__app_label="news",
                content_type__model="article",
                codename__in=[
                    "view_article",
                    "change_article",
                    "delete_article",
                    "approve_article",
                ],
            )
            | Q(
                content_type__app_label="news",
                content_type__model="newsletter",
                codename__in=[
                    "view_newsletter",
                    "change_newsletter",
                    "delete_newsletter",
                ],
            )
        )

        journalist_permissions = Permission.objects.filter(
            Q(
                content_type__app_label="news",
                content_type__model="article",
                codename__in=[
                    "add_article",
                    "view_article",
                    "change_article",
                    "delete_article",
                ],
            )
            | Q(
                content_type__app_label="news",
                content_type__model="newsletter",
                codename__in=[
                    "add_newsletter",
                    "view_newsletter",
                    "change_newsletter",
                    "delete_newsletter",
                ],
            )
        )

        reader_group.permissions.set(reader_permissions)
        editor_group.permissions.set(editor_permissions)
        journalist_group.permissions.set(journalist_permissions)

        self.stdout.write(
            self.style.SUCCESS(
                "Reader, Editor, and Journalist groups were created successfully."
            )
        )
