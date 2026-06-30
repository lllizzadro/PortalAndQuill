# Portal and Quill

Website for **Portal and Quill**, a **fantasy / sci-fi bookstore** owned by the user's friend **Robbie**. Built in **Flask** by the user, who is **learning Flask and web development** (this is their first Flask app).

## How to work on this project (important)

The user is learning and wants to be **guided, not have code written for them**. Hand them one digestible step at a time, explain the *why* (not just the *what*), and let them type and run the code themselves. Show patterns and boilerplate with explanation, but let them fill things in. Let them feel a problem before showing the fix.

**Editing boundary:** Only edit project files when the user *explicitly* asks you to change a specific thing ("refactor X", "add this line", "you make the change"). Treat "let's do X", "suggest", or "review" as requests to **guide**, not to write code. Reading/inspecting files for guidance is always fine; keeping this file current is fine when asked.

## Scope

A **brochure / info site** — no catalog, accounts, or payments (for now).

- **Pages (built & styled):** Home, Events, About the Store, Visit & Contact. (Events added at Robbie's request. The standalone Contact page was merged into Visit — contact is a `mailto:` message box there, no backend.)
- **Pages (later / ideas):** Books & Recommendations, FAQ.

## Design system

- **Mobile-first** — base styles target phones; desktop is layered on via a single `@media (min-width: 760px)` block at the **bottom** of `style.css` (base rules first, media queries last, or a later base rule will quietly override the media query).
- **Theme:** deep green + gold, ornate "fantasy library" — the ChatGPT "render 2" look (rich, not minimalist). Tagline: "Books Beyond Worlds."
- **Colors** — CSS custom properties in `static/css/style.css`, named by role (`--color-bg`, `--color-primary` dark phthalo green, `--color-accent` purple, `--color-gold` antique gold, `--color-surface` lifted-green panel, `--color-text` parchment, `--color-muted`, `--color-eggplant`). `style.css` is the single source of truth for hex values — do NOT duplicate them here.
- **Type:** `--font-display` = Cinzel (headings/wordmark), `--font-body` = EB Garamond (reading); loaded from Google Fonts in `base.html`. Parchment for reading text, muted for secondary/meta. (EB Garamond uses oldstyle numerals by default.)
- **Buttons:** `.btn` = primary (aubergine fill + gold border); `.btn.btn-secondary` = gold outline. Hover lifts/glows; `:focus-visible` gold ring. One primary per view, secondary for lesser actions.
- **Imagery:** real art lives in `static/images/` as optimized JPEGs (hero, event card thumbnails, per-page banners). **Workflow for new art:** convert the source PNG and resize — `sips -s format jpeg -s formatOptions 80 -Z 1600 in.png --out out.jpg` — keep files small (≈<300 KB); the heavy source PNGs are not committed. Transparent overlay textures must stay PNG, not JPEG.
- **Logo:** owner will provide one later; placeholder slot in the header in `base.html`. Favicon is a placeholder gold-portal SVG (`static/favicon.svg`) — swap both when the logo arrives.

## Decisions already settled (don't re-propose)

- **Flat deep-green background** — ambient glow and texture overlays (paper-grain, star-dust) were tried and rejected; the flat color reads best.
- **Headings stay regular Cinzel** — "Cinzel Decorative" was tried and rejected. Oldstyle numerals are already EB Garamond's default, so no `font-variant-numeric` is needed.
- **Uniform gold borders on panels** — a quieter "card hierarchy" tier was tried; the user prefers consistent prominent gold framing (it's part of the identity). Only `.prose` is intentionally borderless (editorial).
- **Contact is `mailto:`** — a real server-side contact form is parked, not wanted yet.
- **Dark map = a CSS `invert()`/`hue-rotate()` filter** on the iframe (Visit page) — intentional, not a bug; it's the cheap "good enough" route. Leaflet + dark tiles is the known upgrade path if a cleaner map is ever wanted.

## Tech stack & structure

- Python 3.14, Flask. Dependencies pinned in `requirements.txt` (includes **gunicorn**, the production server).
- `app.py` — routes: `home` (`/`), `about` (`/about`), `visit` (`/visit`), `events` (`/events`). A module-level `EVENTS` list (list of dicts) is the single source of truth for events; `home` passes `EVENTS[:3]` (preview), `events` passes the full list. An `@app.after_request` hook stamps **security headers + a strict CSP** on every response (see Security).
- `templates/`
  - `base.html` — shared shell (head, header, hamburger nav, footer). Nav is a `nav_links` list looped with `{% for %}`; active link via `request.endpoint`. Footer has wordmark, tagline, an Instagram link, and copyright. Favicon linked here.
  - `_macros.html` — the `page_header(title, intro, kicker, variant)` macro for secondary-page mastheads (kicker + Cinzel title + intro + ✦ divider + constellation SVG). The per-page banner image is set in CSS via `.page-header.<variant>` (e.g. `.page-header.events`), **not** inline. Any template using the macro must `{% import "_macros.html" as ui %}` (imports are per-template, not global).
  - page templates `{% extends "base.html" %}` and fill `{% block content %}`.
- `static/css/style.css` — design tokens + all styles. Reusable components: `.btn`/`.btn-secondary`, `.card`, `.section`, `.prose` (centered reading column), `.page-header`, `.visit-block`, the `.hours`/`.contact` row lists, footer, etc.
- `static/js/nav.js` — animated hamburger nav toggle (transitions `max-height`/`opacity`), plus the Visit page "Email Us" button (builds a `mailto:` to info@portalandquill.com from the textarea; guarded with `if (emailBtn)` so it's harmless on pages without it).
- `static/favicon.svg` — placeholder gold-portal favicon. `static/images/` — optimized JPEGs only.
- Deploy/config files: `Dockerfile`, `.dockerignore`, `fly.toml`, `.github/workflows/fly-deploy.yml`.

## Security

- A Flask `after_request` sets baseline headers (`X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options: DENY`, `Permissions-Policy`) plus a **strict Content-Security-Policy** — no `'unsafe-inline'`; allowlists only Google Fonts (`fonts.googleapis.com`/`fonts.gstatic.com`) and the Google Maps iframe (`www.google.com`/`maps.google.com`). If you add an external resource or any inline script/style, the CSP must be updated or it'll be blocked.
- No backend attack surface (no DB, accounts, or server-processed forms — contact is `mailto:`), so CSRF/input-sanitization/SQLi defenses are intentionally absent.
- **Never run the dev server or `--debug` in production** (the Werkzeug debugger is an RCE vector) — production uses gunicorn. HTTPS is provided automatically by Fly. Run `pip-audit` periodically (and after `pip install`) for dependency CVEs.

## Setup on a new machine (development)

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask run --debug                # serves http://127.0.0.1:5000
```

**macOS note:** port 5000 is occupied by AirPlay Receiver (Control Center), so on a Mac run `flask run --debug --port 5001` and open http://127.0.0.1:5001 instead. Windows has no such conflict — 5000 is fine there.

The `.venv/` folder is **not** committed — it's recreated from `requirements.txt` on each machine. Whenever you `pip install` something new, re-run `pip freeze > requirements.txt` and commit it.

## Deployment (Fly.io)

The site is **live on Fly.io**. Production runs **gunicorn** (`gunicorn app:app --bind 0.0.0.0:8080`) inside the image built from the `Dockerfile`; `fly.toml` sets the internal port (8080), `force_https`, and the app is scaled to **1 machine** (`fly scale count 1`).

- **Auto-deploy:** merging to `main` triggers `.github/workflows/fly-deploy.yml` (GitHub Actions → `flyctl deploy --remote-only`), authenticated by the `FLY_API_TOKEN` repo secret. The user works on a `dev` branch and merges to `main` to ship.
- **Manual deploy:** `fly deploy`. Useful: `fly status`, `fly logs`, `fly open`.
- To run a production-style server locally for testing: `gunicorn app:app --bind 127.0.0.1:8080` (gunicorn is Unix-only — on Windows use `waitress`).

## Current status

The full brochure site is **built, styled, security-hardened, and live on Fly.io with CI/CD**, mobile-first, in the deep-green-and-gold "render 2" look:

- Shared header with responsive **animated** hamburger nav + active-page highlight. Footer: wordmark, "Books Beyond Worlds" tagline, Instagram link, copyright.
- **Home:** full-bleed hero (image with overlaid title) + "Upcoming Events" preview (3 cards from `EVENTS`).
- **Events:** banner masthead + long-form event list (shares `EVENTS`).
- **About:** banner masthead + prose reading column with gold drop cap, signature, and a closing flourish/CTA.
- **Visit & Contact:** banner masthead, Hours + Find Us panels, embedded Google map, and a `mailto:` message box.

Still placeholder: the **logo** (favicon + header slot both ready to swap), some content (event details, About copy, phone number).

**Possible next steps:** swap in the real logo when Robbie delivers it; finalize placeholder content; build the "later" pages (FAQ, Books & Recommendations) reusing the macro/components; the parked backend projects (events database, server-side contact form).
