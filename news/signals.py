from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User


@receiver(post_save, sender=User)
def assign_user_group(sender, instance, **kwargs):
    """Assign the user to the Django group matching their role."""

    if not instance.role:
        return

    role_groups = {
        User.Role.READER: "Reader",
        User.Role.EDITOR: "Editor",
        User.Role.JOURNALIST: "Journalist",
    }

    group_name = role_groups.get(instance.role)

    if not group_name:
        return

    group, _ = Group.objects.get_or_create(
        name=group_name
    )

    instance.groups.clear()
    instance.groups.add(group)