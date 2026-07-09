import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from accounts.models import Profile

pytestmark = pytest.mark.django_db


def test_signup_creates_user_and_logs_in(client):
    response = client.post(
        reverse("signup"),
        {
            "username": "newuser",
            "password1": "StrongPassw0rd!23",
            "password2": "StrongPassw0rd!23",
        },
    )

    assert response.status_code == 302
    assert User.objects.filter(username="newuser").exists()
    assert "_auth_user_id" in client.session


def test_login_authenticates_existing_user(client):
    User.objects.create_user(username="alice", password="StrongPassw0rd!23")

    response = client.post(
        reverse("login"),
        {"username": "alice", "password": "StrongPassw0rd!23"},
    )

    assert response.status_code == 302
    assert "_auth_user_id" in client.session


def test_logout_clears_session(client):
    user = User.objects.create_user(username="bob", password="StrongPassw0rd!23")
    client.force_login(user)

    response = client.post(reverse("logout"))

    assert response.status_code == 302
    assert "_auth_user_id" not in client.session


def test_profile_is_one_to_one_with_user_and_stores_fields():
    user = User.objects.create_user(username="carol", password="StrongPassw0rd!23")

    profile = Profile.objects.create(
        user=user, name="Carol", cohort="2026-A", focus_area="python, django"
    )

    assert profile.user == user
    assert user.profile == profile
    assert profile.focus_area_list == ["python", "django"]


def test_profile_view_shows_own_data(client):
    user = User.objects.create_user(username="dana", password="StrongPassw0rd!23")
    Profile.objects.create(user=user, name="Dana", cohort="2026-B")
    client.force_login(user)

    response = client.get(reverse("profile"))

    assert response.status_code == 200
    assert response.context["profile"].user == user
    assert b"Dana" in response.content


def test_profile_view_never_exposes_another_users_data(client):
    owner = User.objects.create_user(username="erin", password="StrongPassw0rd!23")
    Profile.objects.create(user=owner, name="Erin")
    other = User.objects.create_user(username="frank", password="StrongPassw0rd!23")
    Profile.objects.create(user=other, name="Frank")
    client.force_login(other)

    response = client.get(reverse("profile"))

    assert response.status_code == 200
    assert response.context["profile"].user == other
    assert b"Erin" not in response.content


def test_anonymous_profile_access_redirects_to_login(client):
    response = client.get(reverse("profile"))

    assert response.status_code == 302
    assert response.url.startswith(reverse("login"))


def test_profile_page_offers_a_logout_control(client):
    user = User.objects.create_user(username="hank", password="StrongPassw0rd!23")
    Profile.objects.create(user=user, name="Hank")
    client.force_login(user)

    response = client.get(reverse("profile"))

    assert response.status_code == 200
    assert f'action="{reverse("logout")}"'.encode() in response.content


def test_anonymous_nav_offers_login_and_signup(client):
    response = client.get(reverse("login"))

    assert response.status_code == 200
    assert reverse("signup").encode() in response.content


def test_profile_edit_updates_fields(client):
    user = User.objects.create_user(username="gina", password="StrongPassw0rd!23")
    Profile.objects.create(user=user, name="Gina")
    client.force_login(user)

    response = client.post(
        reverse("profile-edit"),
        {"name": "Gina Updated", "cohort": "2026-C", "focus_area": "django"},
    )

    assert response.status_code == 302
    user.profile.refresh_from_db()
    assert user.profile.name == "Gina Updated"
    assert user.profile.cohort == "2026-C"
    assert user.profile.focus_area == "django"
