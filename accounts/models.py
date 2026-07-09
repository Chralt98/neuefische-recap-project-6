from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    name = models.CharField(max_length=150, blank=True)
    cohort = models.CharField(max_length=150, blank=True)
    focus_area = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated tags, e.g. 'python, django, testing'",
    )

    def __str__(self):
        return f"Profile({self.user.username})"

    @property
    def focus_area_list(self):
        return [tag.strip() for tag in self.focus_area.split(",") if tag.strip()]
