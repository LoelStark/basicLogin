from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"  # change in production


# ---------------- Database ---------------- #

def db_connection():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            number TEXT NOT NULL,
            reason TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


init_db()


# ---------------- Routes ---------------- #

@app.route("/")
def index():
    return redirect(url_for("register"))

    conn = db_connection()
    students = conn.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
    conn.close()

    return render_template("index.html", students=students)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # simple demo authentication
        if username == "admin" and password == "admin":
            session["user"] = username
            return redirect(url_for("index"))

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        number = request.form.get("number")
        reason = request.form.get("reason")

        conn = db_connection()
        conn.execute(
            (name, number, reason),
        )
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)