# CLAUDE.md — Action Health (actionhealth)

This file orients AI assistants and developers to the **actionhealth** Django project: purpose, layout, how to run it, and conventions to preserve when changing code.

There is **no `README.md`** in this repository at the time of writing; treat this document as the primary onboarding reference.

---

## Project purpose

**actionhealth** is a membership-oriented web application for **Action Health International** (AHII–style branding in templates and copy). It provides:

- Public marketing-style pages (home, articles listing, journals/events placeholders, memberships info, etc.).
- **Email-based registration and login** with an extended **member profile** (name, professional prefix, membership tier, demographics, social links, photo).
- Authenticated members can create and manage **articles**, **journals**, and **events** (each tied to the authoring user, with publish flags and slugs for public URLs).

The stack is **server-rendered Django** (templates + static CSS/JS), not a separate SPA.

---

## Tech stack and versions

| Component | Detail |
|-----------|--------|
| **Language** | Python 3 (as required by Django 5.x) |
| **Framework** | **Django 5.0.6** (`requirements.txt`) |
| **Database** | **SQLite** — file at `db.sqlite3` under project root (`BASE_DIR`) |
| **Images** | **Pillow**; **`django-resized`** for resized image fields on `Article` and `Event` |
| **Auth** | Custom user model `account.User` (`AUTH_USER_MODEL`); login identifier is **email** |

**Pinned in `requirements.txt`:** `Django==5.0.6`.  
**Unpinned:** `django-resized`, `Pillow` (install whatever versions pip resolves; consider pinning for reproducible deploys).

---

## Repository layout (high level)

```
actionhealth/          # Django project package (settings, root urls, wsgi/asgi)
base/                  # Public site pages
account/               # Users, profiles, auth, dashboard
article/               # News/blog-style articles
journal/               # Journal entries / publications
event/                 # Events
static/                # Project-wide static files (CSS, JS, images)
manage.py              # Django CLI entrypoint
requirements.txt
db.sqlite3             # Local DB (gitignored)
media/                 # User uploads (gitignored)
```

Templates live under each app: `app_name/templates/app_name/`.  
There are **no global `TEMPLATES['DIRS']`** entries; everything uses `APP_DIRS = True`.

---

## Django apps and responsibilities

### `actionhealth` (project package)

- **`settings.py`** — env loading (`.env`), `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, installed apps, DB, static/media, `LOGIN_URL`, `AUTH_USER_MODEL`, `DJANGORESIZED_DEFAULT_SIZE`.
- **`urls.py`** — mounts each app under a path prefix and serves **media** files in development via `static()`.
- **`wsgi.py` / `asgi.py`** — standard Django entrypoints.

### `base`

- **Role:** Public pages that are not tied to a single content model’s CRUD.
- **Models:** None (`base/models.py` is empty).
- **Views:** Home (`index`) shows latest published journals and events; `articles` lists published articles; other routes render mostly static section templates (`journals`, `honorees`, `trainings`, `events`, `memberships_info`).
- **Templates:** `base/templates/base/` including `base.html`, `index.html`, partials (`navbar`, `footer`, flash messages, etc.).

### `account`

- **Role:** Registration, login/logout, dashboard, profile editing; **custom user** and **profile** models.
- **Decorators:** `user_not_logged_in` redirects authenticated users away from login/register.
- **Forms:** Registration (`UserRegisterForm` + `UserProfileRegisterForm`), profile/user updates (`UserProfileUpdateForm`, `UserUpdateForm`), admin-oriented user forms in `forms.py`.
- **Signals:** `account/signals.py` is largely **commented / inactive** (profile auto-create hooks not connected).
- **Admin:** Custom `UserAdmin` registered for `User` and `Profile`.

### `article`

- **Role:** Article list, detail, add (login required), edit (login required).
- **Signals:** `post_delete` on `Article` deletes the image file from storage (`article/signals.py`); loaded from `ArticleConfig.ready()`.

### `journal`

- **Role:** Journal list, detail, add (login required), edit (login required).
- **Signals:** None registered in `JournalConfig`.

### `event`

- **Role:** Event list, detail, add (login required), edit (login required).
- **Signals:** `post_delete` on `Event` deletes event picture (`event/signals.py`); loaded from `EventConfig.ready()`.

---

## Key models and relationships

### `account.User` (custom user)

- Subclasses **`AbstractBaseUser`** (not `AbstractUser` / `PermissionsMixin`).
- **`USERNAME_FIELD` = `email`** (unique).
- Flags: `is_active`, **`staff`** (drives `is_staff`), **`admin`** (custom superuser flag via `is_admin` property).
- **Timestamps:** `date_created`, `date_updated`.
- **`UserManager`:** `create_user`, `create_staffuser`, `create_superuser` (superuser sets `staff=True` and `admin=True`).
- **Important:** `has_perm` and `has_module_perms` are overridden to always return **`True`**, which bypasses Django’s normal permission checks for this model. Be cautious if you rely on admin permissions beyond “superuser vs not.”

### `account.Profile`

- **`OneToOneField`** to `User` (`related_name='user_profile'`, `null=True` on DB).
- **Required-ish profile fields:** `full_name`, `professional_prefix`, `membership_level` (choices: Fellow / Executive / Associate / Student).
- **Optional / demographic:** `country` (default `"Nigerian"`), `date_of_birth` (stored as **`CharField`**, not `DateField`), `workplace`, `field`, `gender`, `phone_number`, `linkedin_url`, `x_url`, `about_me`, `picture`.
- **`picture`:** `ImageField`; `save()` thumbnails large images with **Pillow** on disk.
- **Note:** `generate_unique_id` and a commented-out `membership_id` exist in code; the **initial migration** still referenced `membership_id` — if your database was created from that migration, the live schema may differ from the current `models.py`. Run `makemigrations` / inspect DB after model edits.

### `article.Article`

- **`ForeignKey`** → `User` (author).
- **Identity / URLs:** `post_code` (short UUID prefix, unique), **`slug`** (from `slugify(title)` on first save, unique), **`title`** (unique).
- **Content:** `sub_title`, `field`, `body`, `post_status`, **`picture`** (`ResizedImageField`).
- **Publishing:** `is_published` (defaults `False`; **`add_article` sets it `True`** on create), `date_created`, `date_published`, `date_updated` (note: `date_published` uses `auto_now_add` in the model).

### `journal.Journal`

- **`ForeignKey`** → `User`.
- **URLs:** `slug` from title on first save; **`title`** unique.
- **Content:** `sub_title`, `abstract`, `keywords`, `full_journal`, `type`, `field`, optional metadata (`reviewed_by`, `link_to_profile`, `contributor_id_number`, `special_note`), `post_status`.
- **Publishing:** Same general pattern as articles (`is_published`; add view sets `True`).

### `event.Event`

- **`ForeignKey`** → `User`.
- **Fields:** `title`, `slug`, `venue`, `fee`, `link`, `date`, `time`, `description`, `post_status`, **`picture`** (`ResizedImageField`), `is_published`, timestamps.

### Relationship summary

```
User (1) ──< (many) Article
User (1) ──< (many) Journal
User (1) ──< (many) Event
User (1) ── (1) Profile  (OneToOne)
```

---

## URL structure

Root router: `actionhealth/urls.py`.

| Prefix | App namespace | Purpose |
|--------|----------------|---------|
| `/` | `base` | Public pages |
| `/account/` | `account` | Auth and member area |
| `/article/` | `article` | Articles |
| `/journal/` | `journal` | Journals |
| `/event/` | `event` | Events |
| `/admin/` | Django admin | Staff admin |

### `base` (`app_name='base'`)

| Path | Name | View |
|------|------|------|
| `/` | `base:index` | Home |
| `/journals/` | `base:journals` | Static section |
| `/articles/` | `base:articles` | Published articles list |
| `/honorees/` | `base:honorees` | Static section |
| `/trainings/` | `base:trainings` | Static section |
| `/events/` | `base:events` | Static section |
| `/memberships/` | `base:memberships_info` | Memberships info |

### `account` (`app_name='account'`)

| Path | Name | View |
|------|------|------|
| `/account/login/` | `account:login_page` | Login |
| `/account/register/` | `account:register` | Register |
| `/account/logout/` | `account:logout` | Logout |
| `/account/dashboard/` | `account:user_dashboard` | Dashboard + inline profile POST handling |
| `/account/edit-profile/` | `account:user_profile` | Dedicated profile edit |

### `article` (`app_name='article'`)

| Path | Name | View |
|------|------|------|
| `/article/` | `article:all_articles` | List published |
| `/article/all/` | `article:all_articles` | Same (duplicate name registration) |
| `/article/all_articles/` | `article:all_articles` | Same |
| `/article/add/` | `article:add_article` | Create (login required) |
| `/article/<slug>/` | `article:article_detail` | Detail (any slug; no draft check in view) |
| `/article/edit/<slug>/` | `article:article_edit` | Edit (login required) |

### `journal` (`app_name='journal'`)

| Path | Name | View |
|------|------|------|
| `/journal/` | `journal:all_journals` | List published |
| `/journal/all_journals/` | `journal:all_journals` | Same |
| `/journal/add/` | `journal:add_journal` | Create (login required) |
| `/journal/<slug>/` | `journal:journal_detail` | Detail |
| `/journal/edit/<slug>/` | `journal:journal_edit` | Edit (login required) |

### `event` (`app_name='event'`)

| Path | Name | View |
|------|------|------|
| `/event/` | `event:all_events` | List published |
| `/event/all/` | `event:all_events` | Same |
| `/event/all_events/` | `event:all_events` | Same |
| `/event/add/` | `event:add_event` | Create (login required) |
| `/event/<slug>/` | `event:event_detail` | Detail |
| `/event/edit/<slug>/` | `event:event_edit` | Edit (login required) |

**Login redirect:** `LOGIN_URL = '/account/login'` (`settings.py`). Use `?next=` on login to return to a protected view after authentication.

**Media (dev):** `MEDIA_URL` is served from `MEDIA_ROOT` via root `urlpatterns`.

---

## Environment variables

Settings read from the **process environment**, optionally primed by a **`.env`** file at:

1. `BASE_DIR / '.env'` (project root, same level as `manage.py`), or  
2. `BASE_DIR.parent / '.env'` (one directory up)

Lines are `KEY=value` (comments `#` and blank lines ignored). Keys are applied with `os.environ.setdefault`, so existing environment values win.

| Variable | Required | Default / behavior |
|----------|----------|-------------------|
| **`DJANGO_SECRET_KEY`** | **Yes** | If missing, Django raises `ImproperlyConfigured` |
| **`DJANGO_DEBUG`** | No | `'True'` / `'1'` / `'yes'` → debug on (default true if unset) |
| **`DJANGO_ALLOWED_HOSTS`** | No | Comma-separated hosts; default `*` (split and stripped) |

**Example `.env` for local development:**

```env
DJANGO_SECRET_KEY=your-secret-key-here-change-in-production
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

`.env` is **gitignored**; do not commit secrets.

---

## Database

- **Engine:** `django.db.backends.sqlite3`
- **File:** `BASE_DIR / 'db.sqlite3'`
- **Migrations:** Per-app under `*/migrations/`

After pulling code or changing models:

```bash
python manage.py migrate
```

---

## How to run locally

1. **Python environment**  
   Create and activate a venv; install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. **Environment**  
   Set `DJANGO_SECRET_KEY` (e.g. in `.env` as above).

3. **Database**  
   ```bash
   python manage.py migrate
   ```

4. **Superuser** (admin uses email + password):

   ```bash
   python manage.py createsuperuser
   ```

5. **Development server**

   ```bash
   python manage.py runserver
   ```

   Visit `http://127.0.0.1:8000/` for the site and `/admin/` for Django admin.

6. **Static files**  
   - Dev: `STATICFILES_DIRS` includes project `static/`.  
   - Production: run `collectstatic` into `STATIC_ROOT` (`staticfiles/`) and serve via your web server.

7. **Media uploads**  
   User uploads go under `media/` (`MEDIA_ROOT`). Ensure the process can write there locally.

---

## Conventions and rules when making changes

### Architecture and style

- **Keep apps focused:** `base` = mostly static/marketing views; `account` = users; content types stay in their own apps.
- **URL names:** Always use **namespaced** reverses: `base:index`, `account:login_page`, `article:article_detail`, etc.
- **Templates:** Place under `app/templates/app/` to match `APP_DIRS` discovery.
- **Shared static assets** live in project **`static/`** (not per-app in this project).

### Auth and security (critical)

- **Login-required views** use `@login_required` from `django.contrib.auth.decorators`.
- **Guest-only views** use `@user_not_logged_in` from `account.decorators`.
- **Login** uses `authenticate(request, email=..., password=...)` — consistent with `USERNAME_FIELD = 'email'`.
- **Known bug:** In `account.views.user_profile`, successful POST redirects to `'account:user-profile'`, but the URL name is **`user_profile`**. Fix redirects to match registered names when touching that view.
- **Authorization gap:** `edit_article`, `edit_journal`, and `edit_event` only check **login**, not **ownership**. They also set `user = request.user` on save, which can **reassign content to the current user**. When editing these views, add proper **object-level permission checks** (e.g. `article.user_id == request.user.pk` or staff flag) and avoid overwriting the author unless that is intentional.

### Models and data

- **Slugs** for articles, journals, and events are generated on **first save** from the title; changing title later does not automatically resync slug in current code.
- **Publishing:** List views filter `is_published=True`, but **detail views** do not consistently hide unpublished items from anonymous users — verify product expectations before exposing slugs.
- **Images:** Article/event images use **`django-resized`**; profile pictures use manual Pillow thumbnailing in `Profile.save()`. Deletion signals clean article/event files on model delete.

### Settings hygiene

- **`DEBUG`** is assigned twice in `settings.py`**; consolidating avoids confusion.
- For production: set **`DJANGO_DEBUG=False`**, restrict **`DJANGO_ALLOWED_HOSTS`**, use a production database and proper static/media hosting, and keep **`DJANGO_SECRET_KEY`** secret.

### Dependencies

- When adding packages, update **`requirements.txt`**; prefer pinning versions for deployment parity.

### Tests

- Each app has a `tests.py` stub; there is little or no test coverage today. Prefer adding tests when fixing auth or data integrity bugs.

---

## Quick reference: `INSTALLED_APPS` order

`django.contrib.*` apps, then: `base`, `account`, `article`, `journal`, `event`.

---

## Optional: django-resized

`DJANGORESIZED_DEFAULT_SIZE = [400, 300]` is set globally; `ResizedImageField` on models may override with explicit `size=[...]`.

<!-- Current state: Project was paused for 2 years. Resuming now with these updates needed: [list them] -->

Rules: Never modify existing migrations. Always create new migrations. Do not change the User model directly — extend it. Run tests after every change.
---

*Generated from the repository structure and source files. Update this file when you change URL patterns, models, or deployment assumptions.*
