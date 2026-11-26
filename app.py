import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-before-deployment")
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "ChangeMe123!")

def get_db():
    import sqlite3
    db = sqlite3.connect("travel.db")
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.execute("""CREATE TABLE IF NOT EXISTS enquiries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, email TEXT NOT NULL, phone TEXT,
        destination TEXT NOT NULL, travel_date TEXT, travellers INTEGER,
        message TEXT, status TEXT DEFAULT 'New',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    db.commit()
    db.close()

init_db()

DESTINATIONS = [
    {"name":"Goa","tag":"Beaches & sunsets","price":"₹8,999","days":"4 days","image":"https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1000&q=85","desc":"Coastal escapes, lively markets and golden-hour beach walks."},
    {"name":"Manali","tag":"Mountains & adventure","price":"₹12,499","days":"5 days","image":"https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=1000&q=85","desc":"Mountain views, pine forests and memorable Himalayan roads."},
    {"name":"Kerala","tag":"Backwaters & nature","price":"₹15,999","days":"6 days","image":"https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1000&q=85","desc":"Slow down among backwaters, tea gardens and tropical scenery."},
    {"name":"Jaipur","tag":"Culture & heritage","price":"₹7,499","days":"3 days","image":"https://images.unsplash.com/photo-1599661046827-dacff0c0f09a?auto=format&fit=crop&w=1000&q=85","desc":"Explore royal architecture, colourful bazaars and local food."},
    {"name":"Ladakh","tag":"Road trips & landscapes","price":"₹24,999","days":"7 days","image":"https://images.unsplash.com/photo-1566837497312-7be4e6e4b7e5?auto=format&fit=crop&w=1000&q=85","desc":"A high-altitude journey through dramatic mountain landscapes."},
    {"name":"Andaman","tag":"Island adventures","price":"₹19,999","days":"6 days","image":"https://images.unsplash.com/photo-1589308078059-be1415eab4c3?auto=format&fit=crop&w=1000&q=85","desc":"Clear waters, island hopping and peaceful tropical beaches."}
]

@app.route("/")
def home():
    return render_template("index.html", destinations=DESTINATIONS)

@app.route("/packages")
def packages():
    return render_template("packages.html", destinations=DESTINATIONS)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        destination = request.form.get("destination", "").strip()
        if not name or not email or not destination:
            flash("Please complete your name, email and destination.", "error")
            return redirect(url_for("contact"))
        db = get_db()
        db.execute("INSERT INTO enquiries (name,email,phone,destination,travel_date,travellers,message) VALUES (?,?,?,?,?,?,?)",
                   (name, email, request.form.get("phone","").strip(), destination,
                    request.form.get("travel_date",""), request.form.get("travellers") or None,
                    request.form.get("message","").strip()))
        db.commit()
        db.close()
        flash("Your travel enquiry has been submitted. Our team will contact you soon.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html", destinations=DESTINATIONS)

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("username") == ADMIN_USERNAME and request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin"))
        flash("Invalid username or password.", "error")
    return render_template("login.html")

@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    db = get_db()
    enquiries = db.execute("SELECT * FROM enquiries ORDER BY id DESC").fetchall()
    db.close()
    return render_template("admin.html", enquiries=enquiries)

@app.route("/admin/status/<int:enquiry_id>", methods=["POST"])
def update_status(enquiry_id):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    status = request.form.get("status", "New")
    if status not in ["New", "Contacted", "Confirmed", "Closed"]:
        status = "New"
    db = get_db()
    db.execute("UPDATE enquiries SET status=? WHERE id=?", (status, enquiry_id))
    db.commit()
    db.close()
    flash("Enquiry status updated.", "success")
    return redirect(url_for("admin"))

@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True)
