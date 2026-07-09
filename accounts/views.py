from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from .forms import ProfileForm, SignupForm
from .models import Profile


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        login(self.request, self.object)
        return response


class OwnProfileMixin(LoginRequiredMixin, SingleObjectMixin):
    model = Profile

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileView(OwnProfileMixin, DetailView):
    template_name = "accounts/profile.html"


class ProfileUpdateView(OwnProfileMixin, UpdateView):
    form_class = ProfileForm
    template_name = "accounts/profile_edit.html"
    success_url = reverse_lazy("profile")
