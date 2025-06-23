from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings


# Custom User Model
class AdminUser(AbstractUser):
    is_admin = models.BooleanField(default=False)  # ✅ Required for permission check

    groups = models.ManyToManyField(
        Group,
        related_name='adminuser_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='adminuser_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    class Meta:
        verbose_name = "Admin User"
        verbose_name_plural = "Admin Users"


# Feedback Group
class FeedbackGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feedback_groups_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Anonymous Feedback Model
class Feedback(models.Model):
    group = models.ForeignKey(
        FeedbackGroup,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    content = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_hidden = models.BooleanField(default=False)  # Used for moderation
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"Feedback for {self.group.name} at {self.submitted_at}"
