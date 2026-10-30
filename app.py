import sqlite3
from contextlib import closing
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# Store the database beside app.py.
DATABASE = Path(__file__).with_name("civicdesk.db")

CATEGORIES = (
    "Street lighting",
    "Roads and pavements",
    "Waste and cleanliness",
    "Other",
)

# Create the table if it does not already exist.
with closing(sqlite3.connect(DATABASE)) as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            location TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Submitted'
        )
    """)
    db.commit()


@app.route("/")
def home():
    with closing(sqlite3.connect(DATABASE)) as db:
        db.row_factory = sqlite3.Row

        records = db.execute(
            "SELECT * FROM requests ORDER BY id DESC"
        ).fetchall()

    return render_template("requests.html", records=records)


@app.route("/new-request", methods=["GET", "POST"])
def new_request():
    if request.method == "POST":
        fields = ("title", "category", "location", "description")
        values = [request.form.get(field, "").strip() for field in fields]

        if not all(values):
            return "Please complete all four fields. Go back and try again.", 400

        if values[1] not in CATEGORIES:
            return "Please choose a category from the list.", 400

        limits = (100, 100, 120, 1500)
        if any(len(value) > limit for value, limit in zip(values, limits)):
            return "One of the fields is too long. Go back and shorten it.", 400

        # Save the form details in SQLite.
        with closing(sqlite3.connect(DATABASE)) as db:
            db.execute("""
                INSERT INTO requests (title, category, location, description)
                VALUES (?, ?, ?, ?)
            """, values)
            db.commit()

        return redirect(url_for("request_saved"), code=303)

    return render_template("new_request.html")


@app.route("/request-saved")
def request_saved():
    return """
        <h1>Request saved!</h1>
        <p>Your fictional request has been saved in CivicDesk.</p>
        <p><a href="/new-request">Add another request</a></p>
        <p><a href="/">Back to home</a></p>
    """


@app.route("/requests/<int:request_id>/status", methods=["POST"])
def update_status(request_id):
    status = request.form.get("status", "")
    allowed_statuses = ("Submitted", "In progress", "Resolved")

    if status not in allowed_statuses:
        return "Please choose a valid status.", 400

    with closing(sqlite3.connect(DATABASE)) as db:
        result = db.execute(
            "UPDATE requests SET status = ? WHERE id = ?",
            (status, request_id)
        )

        if result.rowcount == 0:
            return "Request not found.", 404

        db.commit()

    return redirect(url_for("home"), code=303)


if __name__ == "__main__":
    app.run()