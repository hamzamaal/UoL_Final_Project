from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import get_db_connection

donor_bp = Blueprint("donor", __name__)

@donor_bp.route("/donor_menu")
def donor_menu():
    if "user_id" not in session or session.get("role") != "Donor":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))
    return render_template("donor_menu.html")

@donor_bp.route("/donor/add-donation", methods=["GET", "POST"])
def add_donation():
    if "user_id" not in session or session.get("role") != "Donor":
        flash("Unauthorized access. Please log in as a donor.", "danger")
        return redirect(url_for("auth.login"))

    connection = get_db_connection()
    if not connection:
        flash("Database connection failed.", "danger")
        return redirect(url_for("donor.donor_menu"))

    try:
        cursor = connection.cursor(dictionary=True)
        if request.method == "POST":
            donation_date = request.form.get("donation_date")
            delivery_method = request.form.get("delivery_method")
            delivery_location = request.form.get("delivery_location")
            category = request.form.get("category")
            food_item_name = request.form.get("food_item_name")
            origin = request.form.get("origin")
            expiration_date = request.form.get("expiration_date")
            storage_requirements = request.form.get("storage_requirements")

            # Insert into Donations table
            cursor.execute("""
                INSERT INTO Donations (donation_date, status, delivery_method, delivery_location, recipient_id, donor_id)
                VALUES (%s, 'Pending', %s, %s, NULL, %s)
            """, (donation_date, delivery_method, delivery_location, session["user_id"]))
            connection.commit()
            donation_id = cursor.lastrowid

            # Insert into FoodItems table
            cursor.execute("""
                INSERT INTO FoodItems (name, origin, storage_requirements, expiration_date, category_name, donation_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (food_item_name, origin, storage_requirements, expiration_date, category, donation_id))
            connection.commit()

            flash("Donation added successfully!", "success")
            return redirect(url_for("donor.donor_menu"))

        # Fetch categories for dropdown
        cursor.execute("SELECT category_name FROM Categories")
        categories = cursor.fetchall()

    except Exception as e:
        flash(f"Error adding donation: {e}", "danger")
        categories = []
    finally:
        connection.close()

    return render_template("donor_add_donation.html", categories=categories)


@donor_bp.route("/donor/view-donations", methods=["GET", "POST"])
def view_donations():
    if "user_id" not in session or session.get("role") != "Donor":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))

    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT D.donation_id, D.status, D.delivery_method, D.delivery_location,
                   F.name AS food_item_name, F.category_name, F.expiration_date
            FROM Donations D
            JOIN FoodItems F ON D.donation_id = F.donation_id
            WHERE D.donor_id = %s
            ORDER BY D.donation_date DESC
        """, (session["user_id"],))
        donations = cursor.fetchall()
    except Exception as e:
        flash(f"Error loading donations: {e}", "danger")
        donations = []
    finally:
        connection.close()

    return render_template("donor_view_donations.html", donations=donations)


@donor_bp.route("/donor/view-donation-history")
def view_donation_history():
    if "user_id" not in session or session.get("role") != "Donor":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))

    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT D.donation_id, D.donation_date, D.status,
                   D.delivery_method, D.delivery_location,
                   F.name AS food_item_name, F.expiration_date, F.category_name
            FROM Donations D
            JOIN FoodItems F ON D.donation_id = F.donation_id
            WHERE D.donor_id = %s
            ORDER BY D.donation_date DESC
        """, (session["user_id"],))
        history = cursor.fetchall()
    except Exception as e:
        flash(f"Could not load donation history: {e}", "danger")
        history = []
    finally:
        connection.close()

    return render_template("donor_view_donation_history.html", history=history)


@donor_bp.route("/donor/view-notifications")
def view_notifications():
    if "user_id" not in session or session.get("role") != "Donor":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))

    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT notification_id, message, created_at, is_read
            FROM Notifications
            WHERE user_id = %s AND user_role = 'Donor'
            ORDER BY created_at DESC
        """, (session["user_id"],))
        notifications = cursor.fetchall()
    except Exception as e:
        flash(f"Could not load notifications: {e}", "danger")
        notifications = []
    finally:
        connection.close()

    return render_template("donor_notifications.html", notifications=notifications)


@donor_bp.route("/donor/feedback", methods=["GET", "POST"])
def submit_feedback():
    if "user_id" not in session or session.get("role") != "Donor":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))

    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)

        if request.method == "POST":
            donation_id = request.form.get("donation_id")
            feedback = request.form.get("feedback")
            rating = request.form.get("rating")

            cursor.execute("""
                INSERT INTO DonationFeedback (donation_id, user_id, feedback, rating)
                VALUES (%s, %s, %s, %s)
            """, (donation_id, session["user_id"], feedback, rating))
            connection.commit()

            flash("Feedback submitted successfully!", "success")
            return redirect(url_for("donor.donor_menu"))

        # GET: load donor's past donations for selection
        cursor.execute("""
            SELECT donation_id, donation_date
            FROM Donations
            WHERE donor_id = %s
            ORDER BY donation_date DESC
        """, (session["user_id"],))
        donations = cursor.fetchall()

    except Exception as e:
        flash(f"Error processing feedback: {e}", "danger")
        donations = []
    finally:
        connection.close()

    return render_template("donor_feedback.html", donations=donations)


@donor_bp.route("/donor/delete-donation", methods=["POST"])
def delete_donation():
    if "user_id" not in session or session.get("role") != "Donor":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))

    donation_id = request.form.get("donation_id")
    connection = get_db_connection()

    try:
        cursor = connection.cursor()
        # Optional: Only allow deletion of Pending donations
        cursor.execute("""
            DELETE FROM FoodItems WHERE donation_id = %s
        """, (donation_id,))
        cursor.execute("""
            DELETE FROM Donations WHERE donation_id = %s AND donor_id = %s AND status = 'Pending'
        """, (donation_id, session["user_id"]))
        connection.commit()
        flash("Donation deleted successfully.", "success")

    except Exception as e:
        flash(f"Error deleting donation: {e}", "danger")

    finally:
        connection.close()

    return redirect(url_for("donor.view_donations"))
