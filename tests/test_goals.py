import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from goals.forms import GoalForm, LearningSessionForm
from goals.models import Goal, LearningSession

pytestmark = pytest.mark.django_db


def test_goal_has_default_status_and_timestamps():
    user = User.objects.create_user(username="alice", password="StrongPassw0rd!23")

    goal = Goal.objects.create(user=user, title="Learn Django")

    assert goal.status == "planned"
    assert goal.created_at is not None
    assert goal.updated_at is not None
    assert goal.user == user


def test_goal_status_choices_are_restricted_to_the_three_values():
    assert [choice for choice, _ in Goal.STATUS_CHOICES] == [
        "planned",
        "in-progress",
        "done",
    ]


def test_learning_session_relates_to_its_goal():
    user = User.objects.create_user(username="bob", password="StrongPassw0rd!23")
    goal = Goal.objects.create(user=user, title="Learn Django")

    session = LearningSession.objects.create(
        goal=goal, date="2026-07-01", duration=45, notes="Read docs", tags="python, django"
    )

    assert session.goal == goal
    assert session in goal.sessions.all()
    assert session.tags_list == ["python", "django"]


def test_goal_form_requires_title():
    form = GoalForm(data={"title": "", "description": "", "status": "planned"})

    assert not form.is_valid()
    assert "title" in form.errors


def test_goal_form_rejects_invalid_status():
    form = GoalForm(data={"title": "Learn Django", "description": "", "status": "bogus"})

    assert not form.is_valid()
    assert "status" in form.errors


def test_learning_session_form_rejects_non_positive_duration():
    form = LearningSessionForm(
        data={"date": "2026-07-01", "duration": 0, "notes": "", "tags": ""}
    )

    assert not form.is_valid()
    assert "duration" in form.errors


def test_goal_list_shows_only_the_current_users_goals(client):
    user = User.objects.create_user(username="ivy", password="StrongPassw0rd!23")
    Goal.objects.create(user=user, title="Learn Django")
    client.force_login(user)

    response = client.get(reverse("goal-list"))

    assert response.status_code == 200
    assert list(response.context["goals"]) == list(Goal.objects.filter(user=user))


def test_goal_list_requires_login(client):
    response = client.get(reverse("goal-list"))

    assert response.status_code == 302
    assert response.url.startswith(reverse("login"))


def test_goal_create_assigns_current_user(client):
    user = User.objects.create_user(username="jack", password="StrongPassw0rd!23")
    client.force_login(user)

    response = client.post(
        reverse("goal-create"),
        {"title": "Learn testing", "description": "", "status": "planned"},
    )

    assert response.status_code == 302
    goal = Goal.objects.get(title="Learn testing")
    assert goal.user == user


def test_goal_update_changes_fields(client):
    user = User.objects.create_user(username="kim", password="StrongPassw0rd!23")
    goal = Goal.objects.create(user=user, title="Learn Django")
    client.force_login(user)

    response = client.post(
        reverse("goal-edit", args=[goal.pk]),
        {"title": "Learn Django deeply", "description": "", "status": "in-progress"},
    )

    assert response.status_code == 302
    goal.refresh_from_db()
    assert goal.title == "Learn Django deeply"
    assert goal.status == "in-progress"


def test_goal_delete_removes_it(client):
    user = User.objects.create_user(username="liam", password="StrongPassw0rd!23")
    goal = Goal.objects.create(user=user, title="Learn Django")
    client.force_login(user)

    response = client.post(reverse("goal-delete", args=[goal.pk]))

    assert response.status_code == 302
    assert not Goal.objects.filter(pk=goal.pk).exists()


def test_goal_detail_shows_the_goal(client):
    user = User.objects.create_user(username="mia", password="StrongPassw0rd!23")
    goal = Goal.objects.create(user=user, title="Learn Django")
    client.force_login(user)

    response = client.get(reverse("goal-detail", args=[goal.pk]))

    assert response.status_code == 200
    assert response.context["goal"] == goal


def test_goal_detail_lists_its_sessions(client):
    user = User.objects.create_user(username="nora", password="StrongPassw0rd!23")
    goal = Goal.objects.create(user=user, title="Learn Django")
    LearningSession.objects.create(goal=goal, date="2026-07-01", duration=30)
    client.force_login(user)

    response = client.get(reverse("goal-detail", args=[goal.pk]))

    assert response.status_code == 200
    assert b"30 min" in response.content


def test_session_create_links_it_to_the_goal(client):
    user = User.objects.create_user(username="omar", password="StrongPassw0rd!23")
    goal = Goal.objects.create(user=user, title="Learn Django")
    client.force_login(user)

    response = client.post(
        reverse("session-create", args=[goal.pk]),
        {"date": "2026-07-02", "duration": 60, "notes": "Practice", "tags": "python"},
    )

    assert response.status_code == 302
    session = LearningSession.objects.get(goal=goal)
    assert session.duration == 60
    assert session.tags == "python"


def test_session_update_changes_fields(client):
    user = User.objects.create_user(username="paul", password="StrongPassw0rd!23")
    goal = Goal.objects.create(user=user, title="Learn Django")
    session = LearningSession.objects.create(goal=goal, date="2026-07-01", duration=30)
    client.force_login(user)

    response = client.post(
        reverse("session-edit", args=[session.pk]),
        {"date": "2026-07-01", "duration": 90, "notes": "Updated", "tags": ""},
    )

    assert response.status_code == 302
    session.refresh_from_db()
    assert session.duration == 90
    assert session.notes == "Updated"


def test_session_delete_removes_it(client):
    user = User.objects.create_user(username="quinn", password="StrongPassw0rd!23")
    goal = Goal.objects.create(user=user, title="Learn Django")
    session = LearningSession.objects.create(goal=goal, date="2026-07-01", duration=30)
    client.force_login(user)

    response = client.post(reverse("session-delete", args=[session.pk]))

    assert response.status_code == 302
    assert not LearningSession.objects.filter(pk=session.pk).exists()


def test_goal_list_excludes_other_users_goals(client):
    owner = User.objects.create_user(username="rex", password="StrongPassw0rd!23")
    other = User.objects.create_user(username="sam", password="StrongPassw0rd!23")
    Goal.objects.create(user=other, title="Someone else's goal")
    client.force_login(owner)

    response = client.get(reverse("goal-list"))

    assert list(response.context["goals"]) == []


@pytest.mark.parametrize("url_name", ["goal-detail", "goal-edit", "goal-delete"])
def test_goal_actions_404_for_non_owner(client, url_name):
    owner = User.objects.create_user(username="tina", password="StrongPassw0rd!23")
    other = User.objects.create_user(username="uma", password="StrongPassw0rd!23")
    goal = Goal.objects.create(user=owner, title="Owner's goal")
    client.force_login(other)

    response = client.get(reverse(url_name, args=[goal.pk]))

    assert response.status_code == 404


@pytest.mark.parametrize("url_name", ["session-edit", "session-delete"])
def test_session_actions_404_for_non_owner(client, url_name):
    owner = User.objects.create_user(username="vince", password="StrongPassw0rd!23")
    other = User.objects.create_user(username="wade", password="StrongPassw0rd!23")
    goal = Goal.objects.create(user=owner, title="Owner's goal")
    session = LearningSession.objects.create(goal=goal, date="2026-07-01", duration=30)
    client.force_login(other)

    response = client.get(reverse(url_name, args=[session.pk]))

    assert response.status_code == 404


def test_session_create_404_for_non_owner_of_goal(client):
    owner = User.objects.create_user(username="xena", password="StrongPassw0rd!23")
    other = User.objects.create_user(username="yara", password="StrongPassw0rd!23")
    goal = Goal.objects.create(user=owner, title="Owner's goal")
    client.force_login(other)

    response = client.get(reverse("session-create", args=[goal.pk]))

    assert response.status_code == 404


def test_goal_list_filters_by_status(client):
    user = User.objects.create_user(username="zoe", password="StrongPassw0rd!23")
    done_goal = Goal.objects.create(user=user, title="Finished", status="done")
    Goal.objects.create(user=user, title="Still planning", status="planned")
    client.force_login(user)

    response = client.get(reverse("goal-list"), {"status": "done"})

    assert list(response.context["goals"]) == [done_goal]
