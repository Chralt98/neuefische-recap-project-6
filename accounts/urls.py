from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/edit/", views.ProfileUpdateView.as_view(), name="profile-edit"),
]
