# routes/home_routes.py
from flask import Blueprint, render_template, session, redirect, url_for

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def root():
    return redirect(url_for("home.home_page"))

@home_bp.route("/home")
def home_page():
    if "user" in session and "role" in session:
        if session["role"] == "Donor":
            return redirect(url_for("donor.donor_menu"))
        elif session["role"] == "Recipient":
            return redirect(url_for("recipient_dashboard"))
    return render_template("home.html")


