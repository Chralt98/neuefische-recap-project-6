from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        widgets = {
            "username": forms.TextInput(attrs={"autocomplete": "username"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs["autocomplete"] = "new-password"
        self.fields["password2"].widget.attrs["autocomplete"] = "new-password"


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("name", "cohort", "focus_area")
