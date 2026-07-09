from django import forms

from .models import Goal, LearningSession


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ("title", "description", "status")


class LearningSessionForm(forms.ModelForm):
    class Meta:
        model = LearningSession
        fields = ("date", "duration", "notes", "tags")
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }
