from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import get_db_connection

recipient_bp = Blueprint("recipient", __name__)

@recipient_bp.route("/recipient_menu")
def recipient_menu():
    if "user_id" not in session or session.get("role") != "Recipient":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))
    return render_template("recipient_menu.html")

@recipient_bp.route("/recipient/create-organization", methods=["GET", "POST"])
def create_organization():
    if "user_id" not in session or session.get("role") != "Recipient":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        # Match these to the form field names
        name = request.form.get("org_name")         
        address = request.form.get("address")       
        contact = request.form.get("contact_info")  
        capacity = request.form.get("capacity")     

        connection = get_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO Organization (name, address, contact_info, capacity, registration_date, user_id)
                VALUES (%s, %s, %s, %s, NOW(), %s)
            """, (name, address, contact, capacity, session["user_id"]))
            connection.commit()
            flash("Organization created successfully!", "success")
            return redirect(url_for("recipient.recipient_menu"))
        except Exception as e:
            connection.rollback()
            flash(f"Error creating organization: {e}", "danger")
            print("Insert failed:", e)
        finally:
            connection.close()

    return render_template("recipient_create_organization.html")




@recipient_bp.route("/recipient/request-donation", methods=["GET", "POST"])
def request_donation():
    if "user_id" not in session or session.get("role") != "Recipient":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))

    connection = get_db_connection()
    if not connection:
        flash("Database connection error.", "danger")
        return redirect(url_for("recipient.recipient_menu"))

    try:
        cursor = connection.cursor(dictionary=True)

        if request.method == "POST":
            donation_id = request.form.get("donation_id")

            if not donation_id:
                flash("Please select a donation.", "warning")
                return redirect(url_for("recipient.request_donation"))

            # ✅ Get the recipient's organization ID
            cursor.execute("SELECT organization_id FROM Organization WHERE user_id = %s", (session["user_id"],))
            org = cursor.fetchone()

            if not org:
                flash("You must create an organization before requesting a donation.", "warning")
                return redirect(url_for("recipient.create_organization"))

            organization_id = org["organization_id"]

            # ✅ Update the donation to assign the organization_id as recipient
            cursor.execute("""
                UPDATE Donations
                SET recipient_id = %s, status = 'Completed'
                WHERE donation_id = %s AND recipient_id IS NULL AND status = 'Pending'
            """, (organization_id, donation_id))

            if cursor.rowcount == 0:
                flash("This donation is no longer available.", "warning")
            else:
                connection.commit()
                flash("Donation requested successfully!", "success")

            return redirect(url_for("recipient.recipient_menu"))

        # For GET: fetch only available donations
        cursor.execute("""
            SELECT D.donation_id, D.delivery_method, D.delivery_location,
                   F.name AS food_item_name, F.category_name, F.expiration_date
            FROM Donations D
            JOIN FoodItems F ON D.donation_id = F.donation_id
            WHERE D.status = 'Pending' AND D.recipient_id IS NULL
        """)
        donations = cursor.fetchall()

    except Exception as e:
        flash(f"Error: {e}", "danger")
        donations = []
    finally:
        connection.close()

    return render_template("recipient_request_donation.html", donations=donations)




@recipient_bp.route("/recipient/view-available-donations")
def view_available_donations():
    if "user_id" not in session or session.get("role") != "Recipient":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))

    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT D.donation_id, F.name AS food_item_name, F.category_name,
                   D.delivery_method, D.delivery_location, F.expiration_date
            FROM Donations D
            JOIN FoodItems F ON D.donation_id = F.donation_id
            WHERE D.status = 'Pending' AND D.recipient_id IS NULL
        """)
        donations = cursor.fetchall()
    except Exception as e:
        flash(f"Error loading available donations: {e}", "danger")
        donations = []
    finally:
        connection.close()

    return render_template("recipient_view_available_donations.html", donations=donations)


@recipient_bp.route("/recipient/view-my-requests")
def view_my_requests():
    if "user_id" not in session or session.get("role") != "Recipient":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))

    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM DonationRequests
            WHERE recipient_id = %s
            ORDER BY request_date DESC
        """, (session["user_id"],))
        requests = cursor.fetchall()
    except Exception as e:
        flash(f"Error loading requests: {e}", "danger")
        requests = []
    finally:
        connection.close()

    return render_template("recipient_view_my_requests.html", requests=requests)

@recipient_bp.route("/recipient/view-request-history")
def view_request_history():
    if "user_id" not in session or session.get("role") != "Recipient":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))

    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM DonationRequests
            WHERE recipient_id = %s AND status IN ('Completed', 'Rejected')
            ORDER BY request_date DESC
        """, (session["user_id"],))
        history = cursor.fetchall()
    except Exception as e:
        flash(f"Error loading history: {e}", "danger")
        history = []
    finally:
        connection.close()

    return render_template("recipient_view_request_history.html", history=history)

@recipient_bp.route("/recipient/update-status", methods=["GET", "POST"])
def update_request_status():
    if "user_id" not in session or session.get("role") != "Recipient":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        request_id = request.form.get("request_id")
        new_status = request.form.get("status")

        connection = get_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE DonationRequests
                SET status = %s
                WHERE request_id = %s AND recipient_id = %s
            """, (new_status, request_id, session["user_id"]))
            connection.commit()
            flash("Request status updated.", "success")
        except Exception as e:
            flash(f"Error updating status: {e}", "danger")
        finally:
            connection.close()

        return redirect(url_for("recipient.view_my_requests"))

    # If GET: render the form
    return render_template("recipient_update_status.html")


@recipient_bp.route("/recipient/notifications")
def recipient_notifications():
    if "user_id" not in session or session.get("role") != "Recipient":
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))

    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM Notifications
            WHERE user_id = %s AND user_role = 'Recipient'
            ORDER BY created_at DESC
        """, (session["user_id"],))
        notifications = cursor.fetchall()
    except Exception as e:
        flash(f"Error loading notifications: {e}", "danger")
        notifications = []
    finally:
        connection.close()

    return render_template("recipient_notifications.html", notifications=notifications)

@recipient_bp.route("/recipient/add-feedback", methods=["GET", "POST"])
def recipient_feedback():
    if "user_id" not in session or session.get("role") != "Recipient":
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
            flash("Feedback submitted.", "success")
            return redirect(url_for("recipient.recipient_menu"))

        cursor.execute("""
            SELECT donation_id, donation_date
            FROM Donations
            WHERE recipient_id = %s
            ORDER BY donation_date DESC
        """, (session["user_id"],))
        donations = cursor.fetchall()

    except Exception as e:
        flash(f"Error loading donation list: {e}", "danger")
        donations = []
    finally:
        connection.close()

    return render_template("recipient_add_feedback.html", donations=donations)
