from flask import Flask, render_template, Response, request, redirect

app = Flask(__name__)

SITE_URL = 'https://portalandquill.com'

STRUCTURED_DATA = {
    "@context": "https://schema.org",
    "@type": "BookStore",
    "name": "Portal and Quill",
    "url": SITE_URL,
    "image": SITE_URL + "/static/images/hero.jpg",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "2021 Gallatin Pike N, Suite 130",
        "addressLocality": "Madison",
        "addressRegion": "TN",
        "postalCode": "37115",
        "addressCountry": "US",
    },
    "openingHoursSpecification": [
        {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "10:00",
            "closes": "18:00",
        }
    ],
}

Events = [
    {
    "month": "Date", "day": "TBD", #"Nov", "day": "09",
    "title": "Portal & Quill Soft Opening",
    "when": "TBD",#"Mon, Nov 9 · 12:00 PM",
    "image": "cardBook.jpg",
    "description": "Portal & Quill is opening its doors. Come browse before anyone else, say hello, and help us turn the first page of the story. New friends and new worlds await.",
},
]

@app.route('/')
def home():
    return render_template('home.html', events=Events[:3])

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/visit')
def visit():
    return render_template('visit.html')

@app.route('/events')
def events():
    return render_template('events.html', events=Events)

@app.route('/sitemap.xml')
def sitemap():
    pages = ['home', 'about', 'visit', 'events']
    xml = render_template('sitemap.xml', pages=pages)
    return Response(xml, mimetype="application/xml")

@app.route('/robots.txt')
def robots():
    lines = [
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {SITE_URL}/sitemap.xml",
    ]
    return Response("\n".join(lines), mimetype="text/plain")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.context_processor
def inject_globals():
    return {"site_url": SITE_URL, "structured_data": STRUCTURED_DATA}

@app.before_request
def before_request():
    if ("www" in request.host or "fly.dev" in request.host):
        return redirect(SITE_URL + request.path, code=301)

@app.after_request
def set_security_headers(response):
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    response.headers["Content-Security-Policy"] = (
    "default-src 'self'; "
    "script-src 'self'; "
    "style-src 'self' https://fonts.googleapis.com; "
    "font-src 'self' https://fonts.gstatic.com; "
    "img-src 'self' data:; "
    "frame-src https://www.google.com https://maps.google.com; "
    "connect-src 'self'; "
    "base-uri 'self'; "
    "form-action 'self'; "
    "object-src 'none'; "
    "frame-ancestors 'none'"
    )
    return response