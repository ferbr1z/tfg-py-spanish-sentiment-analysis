# Repository Guidelines

## Project Structure & Module Organization

`main.py` defines the FastAPI application and HTTP routes. Application orchestration lives in `app/`, while `scrapper/` contains the X/Twitter client, compatibility patches, cookies, and tweet-type definitions. Database setup and SQLModel entities are under `database/`; request schemas are in `schemas.py`. Put CSV and Google Sheets integrations in `handlers/`, and sentiment-model code in `sentiment_analyzer/`. Configuration is loaded from `.env` through `config.py`; use `example.env` as the starting template.

## Build, Test, and Development Commands

Activate a virtual environment before running commands. The repository currently has no dependency lock file, so keep dependency changes documented and add a manifest when introducing packages.

- `uvicorn main:app --reload` starts the API locally with automatic reload.
- `python -m scrapper.test` runs the scraper smoke test against recent Paraguayan posts.
- `python -m sentiment_analyzer.test` exercises tweet preprocessing and both analysis models.
- `docker compose up -d n8n` starts the n8n service. The Compose file expects an existing `shared_network` and reachable PostgreSQL service.

The smoke scripts use live services or downloaded ML models; configure credentials and network access before running them.

## Coding Style & Naming Conventions

Follow PEP 8 with four-space indentation. Use `snake_case` for modules, functions, variables, and environment keys; use `PascalCase` for classes and SQLModel entities. Add type hints to public functions and async boundaries. Keep FastAPI routes thin, place reusable work in `app/`, and use `async` database operations consistently. Prefer focused imports and concise docstrings for non-obvious behavior. No formatter or linter is configured, so review diffs for consistent formatting.

## Testing Guidelines

There is no formal test framework or coverage threshold yet. Treat the existing `test.py` modules as manual integration checks, not isolated unit tests. New automated tests should go in `tests/`, use names such as `test_fetch_data.py`, avoid real network calls through fixtures or mocks, and be runnable with `pytest` once that dependency is added.

## Commit & Pull Request Guidelines

Recent commits use short, lowercase summaries such as `test scrapper` and `configurations`. Keep subjects concise and imperative, but make the affected area explicit (for example, `fix scraper pagination`). Pull requests should explain behavior changes, setup or migration needs, and verification commands; link relevant issues and include sample requests or screenshots for API or n8n workflow changes.

## Security & Configuration

Never commit `.env`, authentication tokens, database passwords, OAuth files, or generated data. Copy `example.env` locally, replace all placeholders, and keep Google credentials outside version control.
