import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "students.db")

def connect():
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        roll TEXT,
        branch TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    cur.execute("SELECT * FROM users")
    if cur.fetchone() is None:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", "admin123")
        )

    conn.commit()
    conn.close()

def get_students():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    conn.close()
    return data

def add_student(name, roll, branch):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, roll, branch) VALUES (?, ?, ?)",
        (name, roll, branch)
    )
    conn.commit()
    conn.close()

def get_student(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    data = cur.fetchone()
    conn.close()
    return data

def update_student(id, name, roll, branch):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE students SET name=?, roll=?, branch=? WHERE id=?",
        (name, roll, branch, id)
    )
    conn.commit()
    conn.close()

def delete_student(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

def check_user(username, password):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )
    user = cur.fetchone()
    conn.close()
    return user
