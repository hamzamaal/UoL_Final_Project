# app.py
from flask import Flask, session
from config import Config
from routes.home_routes import home_bp
from routes.auth_routes import auth_bp
from routes.donor_routes import donor_bp
from routes.recipient_routes import recipient_bp
from routes.admin_routes import admin_bp
from routes.public_routes import public_bp

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)

first_request_handled = False

@app.before_request
def clear_session_on_startup():
    global first_request_handled
    if not first_request_handled:
        session.clear()
        first_request_handled = True

app.register_blueprint(recipient_bp)
# Register blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(donor_bp)
app.register_blueprint(public_bp)



if __name__ == "__main__":
    app.run(debug=True)





