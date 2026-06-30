from flask import Flask, render_template, Response

app = Flask(__name__)

SITE_URL = 'https://portalandquill.fly.dev'

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
    "month": "Jul", "day": "07",
    "title": "Author Signing: Brandon Sanderson",
    "when": "Sat, Jul 7 · 2:00 PM",
    "image": "cardBook.jpg",
    "description": "Bestselling fantasy author Brandon Sanderson joins us to sign copies of his latest release and chat with readers. Books available in-store; signing limited to three items per guest.",
},
{
    "month": "Jul", "day": "14",
    "title": "Sci-Fi Book Club: Dune",
    "when": "Sat, Jul 14 · 6:00 PM",
    "image": "cardDune.jpg",
    "description": "Our monthly sci-fi book club tackles Frank Herbert's Dune. Newcomers always welcome — come for the spice-fueled discussion, stay for the coffee.",
},
{
    "month": "Jul", "day": "21",
    "title": "Worldbuilding Workshop",
    "when": "Sat, Jul 21 · 1:00 PM",
    "image": "cardMap.jpg",
    "description": "A hands-on worldbuilding workshop for aspiring fantasy and sci-fi writers. Bring a notebook and an idea; leave with a map, a culture, and a few new friends.",
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