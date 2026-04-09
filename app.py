from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import Config


db = SQLAlchemy()

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(30), nullable=False)   # keep simple (upgrade later)
    time = db.Column(db.String(30), nullable=False)
    party_size = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.get("/")
    def index():
        # Sample content you can replace
        featured = [
            {"name": "Citrus Salmon", "desc": "Charred lemon, herbs, seasonal greens", "price": "₹499"},
            {"name": "Truffle Pasta", "desc": "Creamy sauce, parmesan, black pepper", "price": "₹399"},
            {"name": "Smoked Paneer Tikka", "desc": "House marinade, mint chutney", "price": "₹299"},
        ]
        return render_template("index.html", featured=featured)

    @app.get("/menu")
    def menu():
        menu_sections = [
            {
                "title": "Starters",
                "menu_items": [
                    ("Tomato Basil Soup", "Slow-roasted tomatoes, basil oil", "₹199"),
                    ("Crispy Calamari", "Lemon aioli, herbs", "₹349"),
                    ("Paneer Skewers", "Smoked spices, chutney", "₹279"),
                ],
            },
            {
                "title": "Mains",
                "menu_items": [
                    ("Signature Burger", "House sauce, cheddar, fries", "₹399"),
                    ("Grilled Chicken", "Seasonal veg, jus", "₹449"),
                    ("Veg Bowl", "Quinoa, roasted veg, tahini", "₹329"),
                ],
            },
            {
                "title": "Desserts",
                "menu_items": [
                    ("Chocolate Mousse", "Sea salt, cocoa crumble", "₹199"),
                    ("Cheesecake", "Berry compote", "₹249"),
                ],
            },
        ]
        return render_template("menu.html", menu_sections=menu_sections)

    @app.get("/events")
    def events():
        events_list = [
            {"title": "Grand Opening Night", "date": "Saturday, 7:00 PM", "desc": "Live music + tasting menu"},
            {"title": "Chef’s Table", "date": "Next Friday, 8:30 PM", "desc": "Limited seats, curated course"},
        ]
        return render_template("events.html", events_list=events_list)

    @app.get("/about")
    def about():
        return render_template("about.html")

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()
            message = request.form.get("message", "").strip()

            if not name or not email or not message:
                flash("Please fill all fields.", "error")
                return redirect(url_for("contact"))

            db.session.add(ContactMessage(name=name, email=email, message=message))
            db.session.commit()
            flash("Message received! We’ll get back to you soon.", "success")
            return redirect(url_for("contact"))

        return render_template("contact.html")

    @app.route("/reservations", methods=["GET", "POST"])
    def reservations():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            phone = request.form.get("phone", "").strip()
            date = request.form.get("date", "").strip()
            time = request.form.get("time", "").strip()
            party_size = request.form.get("party_size", "").strip()
            notes = request.form.get("notes", "").strip() or None

            if not (name and phone and date and time and party_size.isdigit()):
                flash("Please enter valid reservation details.", "error")
                return redirect(url_for("reservations"))

            db.session.add(
                Reservation(
                    name=name,
                    phone=phone,
                    date=date,
                    time=time,
                    party_size=int(party_size),
                    notes=notes,
                )
            )
            db.session.commit()
            flash("Reservation requested! We’ll confirm shortly.", "success")
            return redirect(url_for("reservations"))

        return render_template("reservations.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
