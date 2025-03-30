from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import get_db_connection

feedback_bp = Blueprint("feedback", __name__)

@feedback_bp.route("/recipient/feedback", methods=["GET", "POST"])
def submit_feedback():
    if request.method == "POST":
        donation_id = request.form.get("donation_id")
        feedback = request.form.get("feedback")
        rating = request.form.get("rating")

        connection = get_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO DonationFeedback (donation_id, user_id, feedback, rating)
                VALUES (%s, %s, %s, %s)
            """, (donation_id, session["user_id"], feedback, rating))
            connection.commit()
            flash("Feedback submitted.", "success")
            return redirect(url_for("recipient.recipient_menu"))
        except Exception as e:
            flash(f"Error submitting feedback: {e}", "danger")
        finally:
            connection.close()

    return render_template("recipient_add_feedback.html")
