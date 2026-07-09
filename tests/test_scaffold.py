from django.conf import settings


def test_settings_module_resolves():
    assert settings.ROOT_URLCONF == "config.urls"


def test_admin_url_redirects_to_login(client):
    response = client.get("/admin/")
    assert response.status_code == 302
