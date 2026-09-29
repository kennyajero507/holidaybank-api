# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

The Django 6 + Django REST Framework API behind the Holidaybank Expeditions site and dashboard. The Next.js front end (public site plus `/admin` dashboard) is the sibling repo **holidaybank-web** (`../holidaybank-web`). This API was ported from an Express/Prisma API and keeps its endpoints and response shapes. The web app depends on those shapes, so treat them as a contract.

## Commands

```bash
python -m venv .venv && .venv\Scripts\activate    # Python 3.12+ (CI uses 3.13)
pip install -r requirements.txt
cp .env.example .env              # DJANGO_DEBUG=true, ADMIN_PASSWORD (12+ chars)
python manage.py migrate
python manage.py seed             # --no-demo: original-site content only; --reset: wipe and restore
python manage.py runserver 8000

python manage.py test tests                                          # all tests
python manage.py test tests.test_api.AuthTests                       # one class
python manage.py test tests.test_api.AuthTests.test_<name>           # one test
```

CI (`.github/workflows/ci.yml`) runs against PostgreSQL 16: `manage.py check`, `makemigrations --check --dry-run` (commit a migration with every model change), then `test tests`. SQLite is the default locally. Setting `DATABASE_URL` switches to Postgres. Code must behave the same on both. That's why countries, categories and tags are relational rather than Postgres arrays.

Tests (`tests/test_api.py`) are end-to-end HTTP tests. `setUpTestData` runs the real `seed` command, and assertions depend on seeded counts (e.g. 24 tours). If you change seed data (`apps/seed/data/`), expect to update those tests. The `APIClient` has to send `HTTP_ORIGIN='http://localhost:3000'`, or writes are rejected (see below).

Docker: `docker compose --env-file .env.docker up --build` runs Postgres, this API under gunicorn, and `../holidaybank-web`. On Railway, migrations run on every start, and `seed` is run once by hand.

## Architecture

**Layout.** `config/` holds settings and the root URLconf. `apps/` has `common` (shared infrastructure), `accounts` (AdminUser, Role, AuditLog, auth), `catalog` (tours, categories, countries, destinations), `content` (blog, testimonials, FAQs, services, `SiteSettings` singleton), `enquiries`, `media` (`ImageAsset` and uploads) and `seed`. Every app's URLs are mounted under `/api/`. Unmatched `/api/*` paths return the JSON error envelope, even in DEBUG.

**Response envelope.** Every response is `{success: true, data, meta?}` or `{success: false, error: {message, code, details?}}`. Build responses with `send()`/`paginate()`/`page_meta()` from `apps/common/responses.py`. Raise `ApiError.not_found/conflict/forbidden/unauthorized(...)` (`apps/common/exceptions.py`) rather than returning error responses by hand. The DRF exception handler flattens validation errors into `error.details` as `{field: message}`.

**Validation.** DRF serializers are used only as schemas: `validate(Schema, request.data)` returns a cleaned dict. Wire field names are camelCase (what the web app sends). Each resource's `apply()`/`assign()` maps them onto snake_case model attributes. Don't use `source=`.

**Generic CRUD (`apps/common/crud.py`).** Most draft/published collections are declared once as a `Resource` in `apps/{catalog,content}/resources.py` and expanded by `build_views()` into:
- public list and detail by slug (published only)
- `admin/<path>` list/create and `admin/<path>/<uuid>` get/patch/delete
- `admin/<path>/<uuid>/status`
- `admin/<path>/bulk/status` and `admin/<path>/bulk`

Tours, destinations, categories, blog, testimonials, FAQs and services all work this way. Only enquiries, accounts, media and a few catalog views (category tree, countries, related tours) are hand-written. Details of `build_views()`:
- It keeps a slug stable on rename unless a new slug is explicitly sent.
- It maps `ProtectedError` to a 409.
- It revalidates the web cache after writes.

**Cache revalidation, a cross-repo contract.** Each `Resource.tags` returns the Next.js cache tags an object affects (`tours`, `tour:<slug>`, `home`…). `apps/common/revalidate.py` POSTs them to `REVALIDATE_URL` (the web app's `/api/revalidate`) with `x-revalidate-secret`. It does this on transaction commit, in a background thread, and never fails the save. The tag names must match `src/lib/tags.ts` in holidaybank-web. Hand-written views that change public content must call `revalidate()` themselves.

**Auth.**
- Views subclass `PublicView` (no auth) or `AdminView` (`apps/accounts/auth.py`).
- `AdminView` authenticates the `hb_admin_token` httpOnly JWT cookie and re-reads the user and role from the DB on every request. It also enforces `required_permissions`, which is a string or a `{METHOD: perm}` dict.
- Use `require(request, perm)` for checks that depend on the payload. Changing `status` counts as publishing, so an edit that flips status needs both `.edit` and `.publish`.
- Permissions are `resource.verb` strings defined in `apps/accounts/permissions_catalog.py`. Roles are seeded as Administrator (locked), Editor, Author and Travel Consultant. A new resource needs its perms added there.
- The cookie is `SameSite=None; Secure` in production, so `VerifyOriginMiddleware` (`apps/common/middleware.py`) is the real CSRF defence: every non-GET request under `/api/` must carry an `Origin`/`Referer` listed in `WEB_ORIGIN`.

**Enquiries.**
- References are `ENQ-YYMM-NNNN`, allocated under a row lock (`EnquiryReferenceCounter`).
- Pipeline: new → assigned → in progress → quoted → booked / closed.
- Each enquiry has an append-only `EnquiryEvent` timeline. Logic lives in `apps/enquiries/services.py`.
- Public submissions are throttled (`THROTTLE_ENQUIRIES`, default 20/hour). Failed logins are rate-limited per IP.
- Throttle counters live in the Django cache, which is per-process locmem unless `CACHE_URL` (Redis) is set.

**Travel areas and navigation.**
- `TravelArea` (catalog) is a regional tree, groups with areas beneath, linked to tours many-to-many and independent of `TourCategory`. Each area also has a card tag, a teaser (`description`), an image and linked `places`.
- It's served as a tree at `/api/areas`, with distinct published-tour counts and `placeCount`, and filters tours with `?area=<slug>` (a group includes its areas).
- Areas are seeded from `AREAS`/`AREA_DETAILS`/`AREA_TOURS` in `apps/seed/data/catalog.py` and managed in Django admin; there's no dashboard CRUD for them.
- `SiteSettings.navigation` holds the menu arranged in the dashboard, validated by `NavItemSchema`/`NavLinkSchema` in `apps/content/views.py`. Links must be site paths or http(s)/mailto/tel. A top-level item can instead carry a `source` (category/area/destination slug, checked to exist on save), which the web app resolves at render time. The menu is replaced whole on PATCH, and an empty list means the web app builds the menu from categories.

**Content provenance.** Seeded records carry `is_sample` and `source_note`. The web app shows a "Sample" badge for demo content. Don't present generated content as real (no invented ratings, licence numbers or accreditations). `apps/content/defaults.py` holds the `SiteSettings` defaults, which the web app's `src/lib/settings.ts` `FALLBACK` mirrors.

**Media.** Uploads go to `MEDIA_ROOT` (`uploads/`) and are served at `/uploads/` by Django unless `SERVE_MEDIA=false`. Their URLs are built from `PUBLIC_API_URL`. The seeded photographs themselves live in the web repo's `public/images/`. The API only stores their `ImageAsset` records (`apps/seed/data/images.py`).

**Settings.** Everything comes from env (`.env.example`). With `DJANGO_DEBUG` off, the server refuses to start if `DJANGO_SECRET_KEY`/`JWT_SECRET` are still the `dev-only` placeholders. `REVALIDATE_SECRET` must equal the web app's. In production, set `COOKIE_DOMAIN` to the shared parent domain, or have the web app proxy through `/backend`.
