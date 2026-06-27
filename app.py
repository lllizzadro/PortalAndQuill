from flask import Flask, render_template

app = Flask(__name__)

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