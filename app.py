from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

DB_NAME = "students.db"

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            roll TEXT,
            branch TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password)
        VALUES ('admin', 'admin123')
    """)

    conn.commit()
    conn.close()

init_db()

# ---------- LOGIN ----------
def is_logged_in():
    return "user" in session


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?", (u, p)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = u
            return redirect("/")
        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


# ---------- STUDENTS ----------
@app.route("/")
def index():
    if not is_logged_in():
        return redirect("/login")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()

    return render_template("index.html", students=students)


@app.route("/add", methods=["GET", "POST"])
def add():
    if not is_logged_in():
        return redirect("/login")

    if request.method == "POST":
        name = request.form["name"]
        roll = request.form["roll"]
        branch = request.form["branch"]

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, roll, branch) VALUES (?, ?, ?)",
            (name, roll, branch),
        )
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if not is_logged_in():
        return redirect("/login")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        roll = request.form["roll"]
        branch = request.form["branch"]

        cursor.execute(
            "UPDATE students SET name=?, roll=?, branch=? WHERE id=?",
            (name, roll, branch, id),
        )
        conn.commit()
        conn.close()
        return redirect("/")

    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()
    conn.close()

    return render_template("edit.html", student=student)


@app.route("/delete/<int:id>")
def delete(id):
    if not is_logged_in():
        return redirect("/login")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")


# ---------- RUN ----------
if __name__ == "__main__":
    app.run()
