from flask import Flask, render_template, request, redirect, session
import db

app = Flask(__name__)
app.secret_key = "student_management_secret"

db.create_tables()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if db.check_user(username, password):
            session["user"] = username
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid login")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")
    students = db.get_students()
    return render_template("index.html", students=students)

@app.route("/add", methods=["GET", "POST"])
def add():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        name = request.form["name"]
        roll = request.form["roll"]
        branch = request.form["branch"]
        db.add_student(name, roll, branch)
        return redirect("/")
    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if "user" not in session:
        return redirect("/login")

    student = db.get_student(id)

    if request.method == "POST":
        name = request.form["name"]
        roll = request.form["roll"]
        branch = request.form["branch"]
        db.update_student(id, name, roll, branch)
        return redirect("/")

    return render_template("edit.html", student=student)

@app.route("/delete/<int:id>")
def delete(id):
    if "user" not in session:
        return redirect("/login")
    db.delete_student(id)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
