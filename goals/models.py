from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Goal(models.Model):
    STATUS_PLANNED = "planned"
    STATUS_IN_PROGRESS = "in-progress"
    STATUS_DONE = "done"
    STATUS_CHOICES = [
        (STATUS_PLANNED, "Planned"),
        (STATUS_IN_PROGRESS, "In progress"),
        (STATUS_DONE, "Done"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="goals"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PLANNED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class LearningSession(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="sessions")
    date = models.DateField()
    duration = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], help_text="Minutes spent"
    )
    notes = models.TextField(blank=True)
    tags = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated tags, e.g. 'python, django'",
    )

    def __str__(self):
        return f"Session({self.goal.title}, {self.date})"

    @property
    def tags_list(self):
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]
