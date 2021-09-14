from flask import Flask, redirect, request, render_template, session
from app import app

@app.route("/frontpage")
def front_page():
    return render_template("front_page.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")