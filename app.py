from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user, login_user, logout_user, UserMixin
import os
import json

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Configure the PostgreSQL database or SQLite if not provided
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 'postgresql://bilingual_survey_database_user:NdlufoDV4sJwchtQtSagx2q5NzmmLhUI@dpg-cs7q4ktumphs73abpsjg-a/bilingual_survey_database'
)
app.config['SECRET_KEY'] = 'your_secret_key'  # Set your secret key for sessions

db = SQLAlchemy(app)
login_manager = LoginManager(app)

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Survey Response model
class SurveyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    survey_data = db.Column(db.Text, nullable=False)  # Store JSON responses or formatted text
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('responses', lazy=True))

# Create the database tables (if they don't exist yet)
with app.app_context():
    db.create_all()

# Setup Flask-Admin
admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')

# Register models to the admin panel
class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == 'admin'

admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(SurveyResponse, db.session))

# Load the logged-in user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route to serve the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to register a new user
@app.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"success": False, "message": "Request must be JSON"}), 400

    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"success": False, "message": "Username or password missing"}), 400

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"success": False, "message": "Username already exists"}), 409

    # Hash the password
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"success": True, "message": "User registered successfully"})

# Route to login
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"success": False, "message": "Request must be JSON"}), 400

    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"success": False, "message": "Username or password missing"}), 400

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({"success": True, "message": "Login successful!"})
    else:
        return jsonify({"success": False, "message": "Invalid username or password"}), 401

# Route to handle survey submission
@app.route('/survey', methods=['POST'])
def submit_survey():
    if not request.is_json:
        return jsonify({"success": False, "message": "Request must be JSON"}), 400

    data = request.json
    paragraph1 = data.get('paragraph1')
    paragraph2 = data.get('paragraph2')

    if not paragraph1 or not paragraph2:
        return jsonify({"success": False, "message": "Incomplete survey"}), 400

    # Save survey response
    survey_data = {
        "paragraph1": paragraph1,
        "paragraph2": paragraph2
    }
    new_response = SurveyResponse(user_id=current_user.id, survey_data=json.dumps(survey_data))  # Store as JSON string
    db.session.add(new_response)
    db.session.commit()

    return jsonify({"success": True, "message": "Survey submitted successfully!"})

# Route to logout
@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({"success": True, "message": "Logged out successfully."})

if __name__ == '__main__':
    app.run(debug=True)
