# Framework Conventions

- **Framework**: Django (Python) — Django 5.x on Python 3.12+, dependencies managed with `pip` via `requirements.txt`.
- **Frontend**: Django templates only (server-rendered). No SPA, no JS build step. Django `Forms`/`ModelForm` for input, generic class-based views (`ListView`, `CreateView`, `UpdateView`, `DeleteView`) for CRUD.
- **Database**: SQLite for development and tests (zero-config, bundled); PostgreSQL + `psycopg` in Docker/production.
- **Test command**: `pytest` (via `pytest-django`).
- **Lint/format command**: `ruff check .` (lint) and `ruff format .` (format).
- **Migration command**: `python manage.py makemigrations` then `python manage.py migrate`.
- **Dev server command**: `python manage.py runserver`.
- **Idiomatic secret/env storage**: `.env` file read via `django-environ` in `settings.py`. `.env` is git-ignored; `.env.example` is committed. The OpenAI API key is read as `env("OPENAI_API_KEY")` — never a literal in source (see [secrets.md](secrets.md)).
- **Directory layout notes**: `manage.py` at repo root; project config package (`settings.py`, `urls.py`, `wsgi.py`/`asgi.py`); feature apps as separate packages (e.g. `accounts`, `goals`, `resources`, `dashboard`); shared `templates/` and `static/` directories; Python dependencies pinned in `requirements.txt`.
- **Auth**: use Django's built-in `django.contrib.auth` — `django.contrib.auth.views.LoginView`/`LogoutView` wired in `urls.py` (`django.contrib.auth.urls` includes both plus password-reset views), `UserCreationForm` (`django.contrib.auth.forms`) for signup via a custom `CreateView`. `LoginView`'s default template path is `registration/login.html`, so app templates go under `templates/registration/`. Set `LOGIN_REDIRECT_URL`, `LOGIN_URL`, and `LOGOUT_REDIRECT_URL` in `settings.py` rather than passing them per-view. Per-user data isolation on a view is enforced by filtering the queryset/object lookup on `request.user` inside `get_queryset()`/`get_object()` — not by trusting a URL-supplied pk alone.