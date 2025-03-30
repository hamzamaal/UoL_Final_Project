# Import necessary Flask components and Blueprints
from flask import Flask, session
from config import Config  # Configuration class for environment settings (like SECRET_KEY, DB config)
from routes.home_routes import home_bp  # Blueprint for home page routes
from routes.auth_routes import auth_bp  # Blueprint for authentication (login/register) routes
from routes.donor_routes import donor_bp  # Blueprint for donor-specific functionality
from routes.recipient_routes import recipient_bp  # Blueprint for recipient-specific functionality
from routes.admin_routes import admin_bp  # Blueprint for admin panel routes
from routes.public_routes import public_bp  # Blueprint for publicly available routes (about, newsletter, etc.)

# Initialize the Flask application
app = Flask(__name__, static_folder='static')

# Load app configuration from Config class
app.config.from_object(Config)

# A flag to track whether the first request has been handled
first_request_handled = False

# Clear session data when the app receives its first request
@app.before_request
def clear_session_on_startup():
    global first_request_handled
    if not first_request_handled:
        session.clear()  # Clear any lingering session data
        first_request_handled = True  # Set flag to True so this only happens once

# Register all blueprints (modular route handlers)
app.register_blueprint(recipient_bp)  # Routes for recipient users
app.register_blueprint(admin_bp)      # Routes for admin panel
app.register_blueprint(home_bp)       # Home page routes
app.register_blueprint(auth_bp)       # Login, register, logout
app.register_blueprint(donor_bp)      # Donor-specific routes
app.register_blueprint(public_bp)     # Public content (About, Newsletter, etc.)

# Run the Flask development server if this script is executed directly
if __name__ == "__main__":
    app.run(debug=True)  # Debug mode gives you hot reloading and better error messages
