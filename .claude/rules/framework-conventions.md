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