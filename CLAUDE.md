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
- **Type:** `--font-display` = Cinzel (headings/wordmark), `--font-body` = EB Garamond (reading); loaded from Google Fonts in `base.html`. Parchment for reading text, muted for secondary/meta.
- **Imagery:** real art lives in `static/images/` as optimized JPEGs (hero, event card thumbnails, per-page banners). **Workflow for new art:** convert the source PNG and resize — `sips -s format jpeg -s formatOptions 80 -Z 1600 in.png --out out.jpg` — keep files small (≈<300 KB); the heavy source PNGs are not committed.
- **Logo:** owner will provide one later; placeholder slot in the header in `base.html`.

## Tech stack & structure

- Python 3.14, Flask. Dependencies pinned in `requirements.txt`.
- `app.py` — routes: `home` (`/`), `about` (`/about`), `visit` (`/visit`), `events` (`/events`). A module-level `EVENTS` list (list of dicts) is the single source of truth for events; `home` passes `EVENTS[:3]` (preview), `events` passes the full list.
- `templates/`
  - `base.html` — shared shell (head, header, hamburger nav, footer). Nav is a `nav_links` list looped with `{% for %}`; the active link is detected via `request.endpoint`.
  - `_macros.html` — the `page_header(title, intro, kicker, variant)` macro for secondary-page mastheads (kicker + Cinzel title + intro + ✦ divider + constellation SVG). The per-page banner image is set in CSS via `.page-header.<variant>` (e.g. `.page-header.events`), **not** inline. Any template using the macro must `{% import "_macros.html" as ui %}` (imports are per-template, not global).
  - page templates `{% extends "base.html" %}` and fill `{% block content %}`.
- `static/css/style.css` — design tokens + all styles. Reusable components: `.btn`, `.card`, `.section`, `.prose` (centered reading column), `.page-header`, `.visit-block`, the `.hours`/`.contact` row lists, etc.
- `static/js/nav.js` — hamburger nav toggle, plus the Visit page "Email Us" button (builds a `mailto:` to info@portalandquill.com from the textarea; guarded with `if (emailBtn)` so it's harmless on pages without it).
- `static/images/` — optimized JPEGs only.

## Setup on a new machine

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask run --debug                # serves http://127.0.0.1:5000
```

**macOS note:** port 5000 is occupied by AirPlay Receiver (Control Center), so on a Mac run `flask run --debug --port 5001` and open http://127.0.0.1:5001 instead. Windows has no such conflict — 5000 is fine there.

The `.venv/` folder is **not** committed — it's recreated from `requirements.txt` on each machine. Whenever you `pip install` something new, re-run `pip freeze > requirements.txt` and commit it.

## Current status

The full brochure site is **built and styled**, mobile-first, in the deep-green-and-gold "render 2" look:

- Shared header with a responsive hamburger nav + active-page highlight; a minimal footer (just a copyright line for now).
- **Home:** full-bleed hero (image with overlaid title) + an "Upcoming Events" preview (3 cards from `EVENTS`).
- **Events:** banner masthead + long-form event list (shares `EVENTS`).
- **About:** banner masthead + prose reading column with a gold drop cap, signature, and a closing flourish/CTA.
- **Visit & Contact:** banner masthead, Hours + Find Us panels, an embedded Google map, and a `mailto:` message box.

Some content is still placeholder (event details, About copy, the phone number), and the **logo is a placeholder**.

**Possible next steps:** flesh out the footer; deploy the site; swap in the real logo; build the "later" pages (FAQ, Books & Recommendations) reusing the macro/components; the parked backend projects (events database, server-side contact form).
