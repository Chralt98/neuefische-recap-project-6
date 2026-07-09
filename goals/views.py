from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import GoalForm, LearningSessionForm
from .models import Goal, LearningSession


class UserGoalQuerysetMixin(LoginRequiredMixin):
    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)


class GoalListView(UserGoalQuerysetMixin, ListView):
    template_name = "goals/goal_list.html"
    context_object_name = "goals"

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = Goal.STATUS_CHOICES
        context["selected_status"] = self.request.GET.get("status", "")
        return context


class GoalCreateView(LoginRequiredMixin, CreateView):
    model = Goal
    form_class = GoalForm
    template_name = "goals/goal_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("goal-detail", kwargs={"pk": self.object.pk})


class GoalDetailView(UserGoalQuerysetMixin, DetailView):
    template_name = "goals/goal_detail.html"
    context_object_name = "goal"


class GoalUpdateView(UserGoalQuerysetMixin, UpdateView):
    form_class = GoalForm
    template_name = "goals/goal_form.html"

    def get_success_url(self):
        return reverse("goal-detail", kwargs={"pk": self.object.pk})


class GoalDeleteView(UserGoalQuerysetMixin, DeleteView):
    template_name = "goals/goal_confirm_delete.html"

    def get_success_url(self):
        return reverse("goal-list")


class GoalSessionMixin(LoginRequiredMixin):
    def get_goal(self):
        return get_object_or_404(
            Goal, pk=self.kwargs["goal_pk"], user=self.request.user
        )


class LearningSessionCreateView(GoalSessionMixin, CreateView):
    form_class = LearningSessionForm
    template_name = "goals/session_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.goal = self.get_goal()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.goal = self.goal
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["goal"] = self.goal
        return context

    def get_success_url(self):
        return reverse("goal-detail", kwargs={"pk": self.goal.pk})


class UserSessionQuerysetMixin(LoginRequiredMixin):
    def get_queryset(self):
        return LearningSession.objects.filter(goal__user=self.request.user)


class LearningSessionUpdateView(UserSessionQuerysetMixin, UpdateView):
    form_class = LearningSessionForm
    template_name = "goals/session_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["goal"] = self.object.goal
        return context

    def get_success_url(self):
        return reverse("goal-detail", kwargs={"pk": self.object.goal.pk})


class LearningSessionDeleteView(UserSessionQuerysetMixin, DeleteView):
    template_name = "goals/session_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["goal"] = self.object.goal
        return context

    def get_success_url(self):
        return reverse("goal-detail", kwargs={"pk": self.object.goal.pk})
