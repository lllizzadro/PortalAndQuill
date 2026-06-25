# Portal and Quill

Website for **Portal and Quill**, a **fantasy / sci-fi bookstore** owned by the user's friend **Robbie**. Built in **Flask** by the user, who is **learning Flask and web development** (this is their first Flask app).

## How to work on this project (important)

The user is learning and wants to be **guided, not have code written for them**. Hand them one digestible step at a time, explain the *why* (not just the *what*), and let them type and run the code themselves. Show patterns and boilerplate with explanation, but let them fill things in. Let them feel a problem before showing the fix. Don't dump full implementations unless they ask.

## Scope

A **brochure / info site** — no catalog, accounts, or payments (for now).

- **Pages (built):** Home, About the Store, Visit Us, Contact, Events (Events added at owner Robbie's request)
- **Pages (later / ideas):** Books & Recommendations, FAQ

## Design system

- **Mobile-first** — must scale well on phones (viewport meta tag is set in `base.html`).
- **Theme leans into fantasy / sci-fi.**
- **Colors** (defined as CSS custom properties in `static/css/style.css`, named by role):
  - `--color-primary` — dark phthalo green
  - `--color-accent` — purple
  - plus a dark phthalo background (currently "pine," with "emerald black" parked as a commented alternate) and a warm "parchment" text color
  - `style.css` is the single source of truth for hex values — do NOT duplicate them here.
- **Logo:** owner will provide one later; there's a placeholder slot in the header in `base.html`.
- Visual mockups are being produced on another AI platform and will be translated into HTML/CSS.

## Tech stack & structure

- Python 3.14, Flask. Dependencies pinned in `requirements.txt`.
- `app.py` — routes: `home` (`/`), `about` (`/about`), `visit` (`/visit`), `contact` (`/contact`), `events` (`/events`), each rendering the same-named template.
- `templates/` — Jinja templates. `base.html` is the shared shell (head, header, nav, footer); pages `{% extends %}` it and fill `{% block content %}`.
- `static/css/style.css` — theme tokens + global styles.

## Setup on a new machine

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask run --debug                # serves http://127.0.0.1:5000
```

The `.venv/` folder is **not** committed — it's recreated from `requirements.txt` on each machine. Whenever you `pip install` something new, re-run `pip freeze > requirements.txt` and commit it.

## Current status

All five pages (Home, About, Visit, Contact, Events) render from templates that extend `base.html`. The shared header/nav links them all via `url_for`, and the theme stylesheet is wired up. Pages currently hold placeholder content and the layout is essentially unstyled.

**Next step:** style the header/nav and overall layout (mobile-first), and/or fill in real page copy. Visual mockups are pending from another platform and will guide the styling.
