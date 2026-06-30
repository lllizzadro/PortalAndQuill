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
- **One general meta description, not per-page** — a single store-wide `meta_description` (`{% set %}` var in `base.html`, reused by the description + OG + Twitter tags). Per-page descriptions were considered and rejected: not worth it for a 4-page brochure, and Google rewrites the snippet ~⅔ of the time anyway. Don't re-propose per-page.

## Tech stack & structure

- Python 3.14, Flask. Dependencies pinned in `requirements.txt` (includes **gunicorn**, the production server).
- `app.py` — page routes: `home` (`/`), `about` (`/about`), `visit` (`/visit`), `events` (`/events`), plus utility routes `robots` (`/robots.txt`, `text/plain`) and `sitemap` (`/sitemap.xml`, `application/xml`, rendered from the `sitemap.xml` template). A module-level `EVENTS` list (list of dicts) is the single source of truth for events; `home` passes `EVENTS[:3]` (preview), `events` passes the full list. `SITE_URL` constant = the canonical base URL (the `fly.dev` URL now, real domain later); `STRUCTURED_DATA` dict = the JSON-LD `BookStore` schema. An `@app.context_processor` (`inject_globals`) exposes `site_url` + `structured_data` to every template. An `@app.errorhandler(404)` renders the themed `404.html` with a real `404` status. An `@app.after_request` hook stamps **security headers + a strict CSP** on every response (see Security).
- `templates/`
  - `base.html` — shared shell (head, header, hamburger nav, footer). Nav is a `nav_links` list looped with `{% for %}`; active link via `request.endpoint`. Footer has wordmark, tagline, an Instagram link, and copyright. Favicon linked here.
  - `_macros.html` — the `page_header(title, intro, kicker, variant)` macro for secondary-page mastheads (kicker + Cinzel title + intro + ✦ divider + constellation SVG). The per-page banner image is set in CSS via `.page-header.<variant>` (e.g. `.page-header.events`), **not** inline. Any template using the macro must `{% import "_macros.html" as ui %}` (imports are per-template, not global).
  - page templates `{% extends "base.html" %}` and fill `{% block content %}`.
- `static/css/style.css` — design tokens + all styles. Reusable components: `.btn`/`.btn-secondary`, `.card`, `.section`, `.prose` (centered reading column), `.page-header`, `.visit-block`, the `.hours`/`.contact` row lists, footer, etc.
- `static/js/nav.js` — animated hamburger nav toggle (transitions `max-height`/`opacity`), plus the Visit page "Email Us" button (builds a `mailto:` to info@portalandquill.com from the textarea; guarded with `if (emailBtn)` so it's harmless on pages without it).
- `static/favicon.svg` — placeholder gold-portal favicon. `static/images/` — optimized JPEGs only.
- Deploy/config files: `Dockerfile`, `.dockerignore`, `fly.toml`, `.github/workflows/fly-deploy.yml`.

## Security

- A Flask `after_request` sets baseline headers (`Strict-Transport-Security` (HSTS, `max-age=31536000`), `X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options: DENY`, `Permissions-Policy`) plus a **strict Content-Security-Policy** — no `'unsafe-inline'`; allowlists only Google Fonts (`fonts.googleapis.com`/`fonts.gstatic.com`) and the Google Maps iframe (`www.google.com`/`maps.google.com`). If you add an external resource or any inline script/style, the CSP must be updated or it'll be blocked.
- No backend attack surface (no DB, accounts, or server-processed forms — contact is `mailto:`), so CSRF/input-sanitization/SQLi defenses are intentionally absent.
- **Never run the dev server or `--debug` in production** (the Werkzeug debugger is an RCE vector) — production uses gunicorn. HTTPS is provided automatically by Fly. Run `pip-audit` periodically (and after `pip install`) for dependency CVEs.

## SEO & hardening roadmap

Adapted from the user's other project (a portfolio site *with* a backend/guestbook). The big difference: Portal and Quill is a **backend-less brochure site**, so the whole class of form/DB/session defenses doesn't apply here.

**Done — shipped & live on Fly (2026-06-30):**
- **HSTS** — `Strict-Transport-Security: max-age=31536000` in `after_request`. (Still holding off on `preload`/`includeSubDomains` until the custom domain is final.)
- **Meta description** — a single **general** description (see Decisions for why not per-page).
- **Open Graph + Twitter Card** (`summary_large_image`) in `base.html` head — title via `self.title()`, description via the shared `meta_description` var, `og:url` = `site_url + request.path`, `og:image` = interim `hero.jpg` (branded 1200×630 pending the logo).
- **JSON-LD** — `BookStore` schema as a Python dict (`STRUCTURED_DATA`), injected via context processor, rendered with `| tojson`. **Phone omitted** until the real number lands. The inline `<script type="application/ld+json">` is a *data block*, so it needs **no** CSP change.
- **Themed 404** — `templates/404.html` (uses `page_header` macro with `variant="notfound"` → `border-bottom: none`), served by `@app.errorhandler(404)` returning a real `404` status.
- **`robots.txt` + `sitemap.xml`** — both served as **routes** (not static files) built from `SITE_URL`; robots `text/plain`, sitemap `application/xml` from a Jinja template looping the 4 page endpoints. Sitemap is intentionally minimal (`<loc>` only — no fabricated `lastmod`/`changefreq`/`priority`).
- **`noopener` audit** — footer Instagram link is now `rel="noopener noreferrer"` (the only external `_blank` link).
- **Deps cleanup** — `Flask-WTF`/`WTForms` removed from `requirements.txt` (unused; were stale-listed and not even installed).

**Implementation note (done):** canonical / `og:url` / sitemap URLs are built from the single **`SITE_URL`** constant in `app.py` (the `fly.dev` URL now; flip to the real domain later — one edit cascades everywhere). This sidesteps **ProxyFix** (we never derive absolute URLs from the proxied request).

**Deferred — needs the custom domain (pending from Robbie):**
- Canonical tag's final *value* + a **canonical-host 301 redirect** (www + old `fly.dev` → apex, one canonical URL).
- Swap hardcoded `fly.dev` → the real domain throughout.
- **Google Search Console** — submit sitemap, request indexing.
- **Cloudflare** proxy (Full strict) + **DNSSEC** — only configurable once the domain is on Cloudflare.
- **SPF/DMARC** — only if a real mailbox is set up on the domain (contact is `mailto:`, so the site sends no mail itself).

**Deferred — needs the logo (pending from Robbie):**
- Swap the placeholder favicon for the real mark.
- A properly **branded OG image** (1200×630). An interim one cut from existing art is fine in the meantime.

**Not applicable now — would only matter if a backend is ever added** (server-side contact form, events DB, accounts/sessions). Revisit these *together* if that day comes:
- **CSRF** (`CSRFProtect` / Flask-WTF) + `{{ csrf_token() }}`, **honeypot** field — defend server-processed forms.
- **`SECRET_KEY` via env** — signs sessions/flash/CSRF; nothing to sign yet.
- **Parameterized SQL** — no database.
- **Rate limiting** — no abusable endpoint on a static brochure.
- Off-page "inbound links (GitHub/LinkedIn)" — the bookstore equivalent is the Instagram bio link + a **Google Business Profile** + local directories; that's the owner's task, later.

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

The full brochure site is **built, styled, SEO- and security-hardened, and live on Fly.io with CI/CD**, mobile-first, in the deep-green-and-gold "render 2" look:

- Shared header with responsive **animated** hamburger nav + active-page highlight. Footer: wordmark, "Books Beyond Worlds" tagline, Instagram link, copyright.
- **Home:** full-bleed hero (image with overlaid title) + "Upcoming Events" preview (3 cards from `EVENTS`).
- **Events:** banner masthead + long-form event list (shares `EVENTS`).
- **About:** banner masthead + prose reading column with gold drop cap, signature, and a closing flourish/CTA.
- **Visit & Contact:** banner masthead, Hours + Find Us panels, embedded Google map, and a `mailto:` message box.

Still placeholder: the **logo** (favicon + header slot both ready to swap), some content (event details, About copy, phone number).

**Possible next steps:** the SEO/hardening **"Do now" set is shipped** — what remains on that roadmap is **domain-gated** (canonical 301 + flip `SITE_URL`, Search Console, Cloudflare/DNSSEC, SPF/DMARC) and **logo-gated** (real favicon, branded 1200×630 OG image), plus dropping the **real phone** into the JSON-LD + Visit page once Robbie provides it. Beyond that: swap in the real logo, finalize placeholder content, build the "later" pages (FAQ, Books & Recommendations) reusing the macro/components, and the parked backend projects (events database, server-side contact form).
