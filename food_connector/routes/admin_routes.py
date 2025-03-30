from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import get_db_connection
import mysql.connector

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/dashboard")
def admin_dashboard():
    if session.get("role") != "Admin":
        flash("Unauthorized access. Please log in as Admin.", "danger")
        return redirect(url_for("auth.login"))

    return render_template("admin_dashboard.html", username=session.get("username"))

@admin_bp.route("/admin/view-donation-statistics", methods=["GET"])
def view_donation_statistics():
    connection = get_db_connection()
    if not connection:
        flash("Database connection failed.", "danger")
        return redirect(url_for("admin.admin_dashboard"))

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                CURDATE() AS stat_date,
                COUNT(*) AS total_donations,
                SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed_donations,
                SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END) AS pending_donations,
                SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_donations
            FROM Donations
        """)
        statistics = cursor.fetchone()
        flash("Statistics retrieved successfully!", "success")
        return render_template("admin_donation_statistics.html", statistics=statistics)
    except mysql.connector.Error as err:
        flash(f"Error retrieving statistics: {err}", "danger")
        return render_template("admin_donation_statistics.html", statistics=None)
    finally:
        connection.close()

@admin_bp.route("/admin/view-user-logs", methods=["GET"])
def view_user_logs():
    connection = get_db_connection()
    if not connection:
        flash("Database connection failed.", "danger")
        return redirect(url_for("admin.admin_dashboard"))

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                ua.action_id,
                u.username,
                u.role,
                ua.action_type,
                ua.action_details,
                ua.action_timestamp
            FROM UserActions ua
            JOIN User u ON ua.user_id = u.user_id
            ORDER BY ua.action_timestamp DESC;
        """)
        logs = cursor.fetchall()
        flash("User activity logs retrieved successfully!", "success")
        return render_template("admin_user_logs.html", logs=logs)
    except mysql.connector.Error as err:
        flash(f"Error retrieving user logs: {err}", "danger")
        return render_template("admin_user_logs.html", logs=None)
    finally:
        connection.close()

@admin_bp.route("/admin/delete-user", methods=["GET", "POST"])
def delete_user():
    if session.get("role") != "Admin":
        flash("Unauthorized access. Please log in as Admin.", "danger")
        return redirect(url_for("auth.login"))

    connection = get_db_connection()
    if not connection:
        flash("Database connection failed. Please try again later.", "danger")
        return redirect(url_for("admin.admin_dashboard"))

    try:
        cursor = connection.cursor(dictionary=True)
        if request.method == "POST":
            user_id_to_delete = request.form.get("user_id")

            if user_id_to_delete == str(session.get("user_id")):
                flash("You cannot delete your own account.", "danger")
                return redirect(url_for("admin.delete_user"))

            cursor.execute("DELETE FROM User WHERE user_id = %s", (user_id_to_delete,))
            connection.commit()

            if cursor.rowcount > 0:
                flash(f"User ID {user_id_to_delete} deleted successfully.", "success")
            else:
                flash(f"No matching user found for ID {user_id_to_delete}.", "warning")

            return redirect(url_for("admin.delete_user"))

        cursor.execute("SELECT user_id, username, email, role FROM User WHERE user_id != %s", (session["user_id"],))
        users = cursor.fetchall()
    except mysql.connector.Error as err:
        flash(f"Error deleting user: {err}", "danger")
        users = []
    finally:
        connection.close()

    return render_template("admin_delete_user.html", users=users)

@admin_bp.route("/admin/delete-activity-logs", methods=["POST"])
def delete_activity_logs():
    if session.get("role") != "Admin":
        flash("Unauthorized access. Please log in as Admin.", "danger")
        return redirect(url_for("auth.login"))

    connection = get_db_connection()
    if not connection:
        flash("Database connection failed. Please try again later.", "danger")
        return redirect(url_for("admin.view_user_logs"))

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM UserActions")
        connection.commit()

        if cursor.rowcount > 0:
            flash("All activity logs have been cleared successfully.", "success")
        else:
            flash("No activity logs found to delete.", "info")
    except mysql.connector.Error as err:
        flash(f"Error clearing activity logs: {err}", "danger")
    finally:
        connection.close()

    return redirect(url_for("admin.view_user_logs"))
