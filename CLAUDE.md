# CLAUDE.md

Project map for the Learning Companion app. See `.claude/rules/` for pipeline conventions (framework conventions, TDD, secrets).

## Commands

```bash
python3 -m venv .venv && source .venv/bin/activate   # create/activate virtualenv
pip install -r requirements.txt                       # install dependencies
python manage.py makemigrations                       # generate migrations for model changes
python manage.py migrate                              # run migrations
python manage.py runserver                             # start dev server (http://127.0.0.1:8000/)
pytest                                                  # run test suite
ruff check .                                            # lint
ruff format .                                           # format
```

## Architecture

- Django project scaffolded with `django-admin startproject config .` — project config package lives in `config/` (`settings.py`, `urls.py`, `wsgi.py`, `asgi.py`); `manage.py` at repo root.
- Feature apps: `accounts` (auth + profile). `goals`, `resources`, `dashboard` still to be added.
- `accounts` app: `Profile` model (one-to-one with Django's `User`; fields `name`, `cohort`, `focus_area` — the latter a comma-separated `CharField`, not a separate tag model/library). Signup (`SignupView`, `accounts/forms.py::SignupForm`) and profile view/edit (`ProfileView`, `ProfileUpdateView`) live in `accounts`; login/logout use Django's built-in `django.contrib.auth.urls` views directly (wired in `config/urls.py`, no custom code). Profile views always resolve to `request.user.profile` — there's no URL parameter for another user's profile, so cross-user access is blocked structurally rather than via a permission check.
- `LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL` are set in `config/settings.py`. Templates: project-wide `templates/registration/` for Django's built-in auth views (e.g. `login.html`), app-local `accounts/templates/accounts/` for `accounts`' own views.
- Database: SQLite (`db.sqlite3`, git-ignored) for local dev, per `DATABASES` in `config/settings.py`.
- Tests live in `tests/`, run via `pytest` + `pytest-django` (`pytest.ini` points `DJANGO_SETTINGS_MODULE` at `config.settings`).
