from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import get_db_connection
import re
import mysql.connector

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        connection = get_db_connection()
        if not connection:
            flash("Database connection failed. Please try again.", "danger")
            return render_template("login.html")

        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM User WHERE email = %s AND password_hash = SHA2(%s, 256)"
            cursor.execute(query, (email, password))
            user = cursor.fetchone()

            if user:
                session["user_id"] = user["user_id"]
                session["username"] = user["username"]
                session["role"] = user["role"]

                cursor.execute("UPDATE User SET last_login = NOW() WHERE user_id = %s", (user["user_id"],))
                connection.commit()

                if user["role"] == "Donor":
                    return redirect(url_for("donor.donor_menu"))
                elif user["role"] == "Recipient":
                    return redirect(url_for("recipient.recipient_menu"))
                elif user["role"] == "Admin":
                    return redirect(url_for("admin.admin_dashboard"))  # Add admin routes if needed
            else:
                flash("Invalid email or password. Please try again.", "danger")
        except Exception as e:
            flash(f"Login error: {e}", "danger")
        finally:
            connection.close()

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        phone = request.form.get("phone")
        role = request.form.get("role")

        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        phone_regex = r'^\d{10,15}$'

        if not re.match(email_regex, email):
            flash("Invalid email format. Please try again.", "danger")
            return render_template("register.html")
        if not re.match(phone_regex, phone):
            flash("Invalid phone number. Please enter 10-15 digits.", "danger")
            return render_template("register.html")
        if role not in ["Donor", "Recipient"]:
            flash("Invalid role selected. Please choose a valid option.", "danger")
            return render_template("register.html")

        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()

                check_query = "SELECT * FROM User WHERE username = %s OR email = %s"
                cursor.execute(check_query, (username, email))
                if cursor.fetchone():
                    flash("Username or email already exists. Please try again.", "danger")
                    return render_template("register.html")

                query = """
                    INSERT INTO User (username, email, password_hash, phone_number, role)
                    VALUES (%s, %s, SHA2(%s, 256), %s, %s)
                """
                cursor.execute(query, (username, email, password, phone, role))
                connection.commit()

                flash("Registration successful! Please log in.", "success")
                return redirect(url_for("auth.login"))

            except mysql.connector.Error as err:
                if "Duplicate entry" in str(err):
                    flash("Username or email already exists. Please try again.", "danger")
                else:
                    flash(f"Database error: {err}", "danger")
            finally:
                cursor.close()
                connection.close()
        else:
            flash("Database connection failed. Please try again later.", "danger")

    return render_template("register.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/profile")
def profile():
    if "user_id" not in session:
        flash("You must be logged in to view your profile.", "danger")
        return redirect(url_for("auth.login"))

    return render_template("profile.html")  # create profile.html as needed
