import os
import json
import requests
from flask_session import Session

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from config.firebase_config import initialize_firebase, verify_firebase_token
from config.config import GROQ_API_KEY, COLLEGE_INFO

# ✅ Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_fallback_secret_key')

# ✅ Configure session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

# ✅ Initialize Firebase
initialize_firebase()

# ✅ Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ✅ User model for Flask-Login
class User(UserMixin):
    def __init__(self, uid, email):
        self.id = uid
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login with email support"""
    # Simulate retrieving the user from DB (replace with DB query)
    user_email = session.get('email')
    return User(user_id, user_email)

# ===============================
# ✅ Routes
# ===============================

@app.route('/')
def index():
    return redirect(url_for('login'))

# 🔥 Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login route with Firebase token verification"""
    if request.method == 'GET':
        return render_template('login.html')

    id_token = request.form.get('idToken')

    if not id_token:
        return jsonify({"success": False, "message": "Missing ID token"})

    decoded_token = verify_firebase_token(id_token)
    
    if decoded_token:
        user = User(decoded_token['uid'], decoded_token['email'])
        login_user(user)
        session['email'] = decoded_token['email']  # Store email in session
        return jsonify({"success": True, "message": "Login successful"})

    return jsonify({"success": False, "message": "Invalid token"})

# 🔥 Signup route
@app.route('/signup', methods=['POST'])
def signup():
    """Signup route with full name capture"""
    id_token = request.form.get('idToken')
    full_name = request.form.get('fullName')
    email = request.form.get('email')

    if not id_token or not full_name or not email:
        return jsonify({"success": False, "message": "Missing fields"})

    decoded_token = verify_firebase_token(id_token)
    if decoded_token:
        user = User(decoded_token['uid'], email)
        login_user(user)
        session['email'] = email
        return jsonify({
            "success": True,
            "message": "Signup successful",
            "full_name": full_name
        })

    return jsonify({"success": False, "message": "Signup failed"})

# 🔥 Logout route
@app.route('/logout')
@login_required
def logout():
    """Logout route"""
    logout_user()
    session.pop('email', None)
    return redirect(url_for('login'))

# 🔥 Chat route
@app.route('/chat')
@login_required
def chat():
    """Render chat interface"""
    return render_template('index.html')

# ===============================
# ✅ Groq Integration
# ===============================

def get_groq_response(user_query, system_prompt=None):
    """Get a response from Groq API"""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [{"role": "user", "content": user_query}]
    
    if system_prompt:
        messages.insert(0, {"role": "system", "content": system_prompt})

    data = {
        "model": "llama3-70b-8192",
        "messages": messages,
        "temperature": 0.5,
        "max_tokens": 500
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# 🔥 Handle chat queries
@app.route("/ask", methods=["POST"])
@login_required
def ask():
    """Handle user query and return response"""
    user_query = request.form.get("query", "")

    # ✅ Create system prompt with college info
    system_prompt = (
        f"You are a helpful college assistant for {COLLEGE_INFO['name']}.\n"
        f"Use the following information to answer questions:\n"
        f"College Name: {COLLEGE_INFO['name']}\n"
        f"Location: {COLLEGE_INFO['location']}\n"
        f"Founded: {COLLEGE_INFO['founded']}\n"
        f"Popular Programs: {', '.join(COLLEGE_INFO['popular_programs'])}\n"
        f"Tuition: {COLLEGE_INFO['tuition']}\n"
        f"Application Deadline: {COLLEGE_INFO['application_deadline']}\n"
        f"Contact Information: {COLLEGE_INFO['contact']}\n\n"
        f"IMPORTANT: Keep responses brief (1-3 sentences). If unsure, suggest contacting admissions."
    )

    response = get_groq_response(user_query, system_prompt)
    
    return jsonify({"response": response})

# ===============================
# ✅ Start server
# ===============================

if __name__ == "__main__":
    app.run(debug=True, port=5000)
