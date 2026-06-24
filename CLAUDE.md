# Portal and Quill

Website for **Portal and Quill**, a friend's **fantasy / sci-fi bookstore**. Built in **Flask** by an owner who is **learning Flask and web development** (this is their first Flask app).

## How to work on this project (important)

The user is learning and wants to be **guided, not have code written for them**. Hand them one digestible step at a time, explain the *why* (not just the *what*), and let them type and run the code themselves. Show patterns and boilerplate with explanation, but let them fill things in. Let them feel a problem before showing the fix. Don't dump full implementations unless they ask.

## Scope

A **brochure / info site** — no catalog, accounts, or payments (for now).

- **Pages (phase 1):** Home, About the Store, Visit Us, Contact
- **Pages (later):** Events, Books & Recommendations, FAQ

## Design system

- **Mobile-first** — must scale well on phones (viewport meta tag is set in `base.html`).
- **Theme leans into fantasy / sci-fi.**
- **Colors** (defined as CSS custom properties in `static/css/style.css`, named by role):
  - `--color-primary` — dark phthalo green
  - `--color-accent` — purple
  - plus dark/stone-gray/black backgrounds and a warm "parchment" text color
  - These hex values are placeholders to be tuned against real mockups.
- **Logo:** owner will provide one later; there's a placeholder slot in the header in `base.html`.
- Visual mockups are being produced on another AI platform and will be translated into HTML/CSS.

## Tech stack & structure

- Python 3.14, Flask. Dependencies pinned in `requirements.txt`.
- `app.py` — routes (currently just `home()` at `/`).
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

Home page renders from `home.html` extending `base.html`, with the theme stylesheet wired up via `url_for`.

**Next step:** add the About / Visit Us / Contact routes in `app.py` and the matching templates, then add the nav links in `base.html`.
