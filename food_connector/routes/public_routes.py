from flask import Blueprint, render_template

public_bp = Blueprint('public', __name__)

@public_bp.route("/newsletter", endpoint="newsletter")
def newsletter():
    return render_template("newsletter.html")

@public_bp.route("/donate-food", endpoint="donate_food")
def donate_food():
    return render_template("donate_food.html")

@public_bp.route('/about', endpoint="about")
def about():
    return render_template('about.html')

@public_bp.route("/ambassadors")
def ambassadors():
    return render_template("ambassadors.html")

