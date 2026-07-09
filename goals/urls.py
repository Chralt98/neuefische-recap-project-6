from django.urls import path

from . import views

urlpatterns = [
    path("", views.GoalListView.as_view(), name="goal-list"),
    path("new/", views.GoalCreateView.as_view(), name="goal-create"),
    path("<int:pk>/", views.GoalDetailView.as_view(), name="goal-detail"),
    path("<int:pk>/edit/", views.GoalUpdateView.as_view(), name="goal-edit"),
    path("<int:pk>/delete/", views.GoalDeleteView.as_view(), name="goal-delete"),
    path(
        "<int:goal_pk>/sessions/new/",
        views.LearningSessionCreateView.as_view(),
        name="session-create",
    ),
    path(
        "sessions/<int:pk>/edit/",
        views.LearningSessionUpdateView.as_view(),
        name="session-edit",
    ),
    path(
        "sessions/<int:pk>/delete/",
        views.LearningSessionDeleteView.as_view(),
        name="session-delete",
    ),
]
