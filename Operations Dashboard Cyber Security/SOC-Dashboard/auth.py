from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3
import hashlib

auth_bp = Blueprint("auth", __name__)

def get_db():
    return sqlite3.connect("database.db")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users VALUES (?,?)", (username, hashed_password))
        db.commit()
        db.close()

        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
        user = cursor.fetchone()
        db.close()

        if user:
            session["user"] = username
            return redirect(url_for("dashboard"))

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("auth.login"))
