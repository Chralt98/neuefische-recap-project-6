# CLAUDE.md

Project map for the Learning Companion app. See `.claude/rules/` for pipeline conventions (framework conventions, TDD, secrets).

## Commands

```bash
python3 -m venv .venv && source .venv/bin/activate   # create/activate virtualenv
pip install -r requirements.txt                       # install dependencies
python manage.py migrate                              # run migrations
python manage.py runserver                             # start dev server (http://127.0.0.1:8000/)
pytest                                                  # run test suite
ruff check .                                            # lint
ruff format .                                           # format
```

## Architecture

- Django project scaffolded with `django-admin startproject config .` — project config package lives in `config/` (`settings.py`, `urls.py`, `wsgi.py`, `asgi.py`); `manage.py` at repo root.
- No feature apps yet (`accounts`, `goals`, `resources`, `dashboard` will be added as they're built).
- Database: SQLite (`db.sqlite3`, git-ignored) for local dev, per `DATABASES` in `config/settings.py`.
- Tests live in `tests/`, run via `pytest` + `pytest-django` (`pytest.ini` points `DJANGO_SETTINGS_MODULE` at `config.settings`).
