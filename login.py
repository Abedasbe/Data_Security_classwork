# login.py

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import hashlib
from pathlib import Path

app = Flask(__name__)
app.secret_key = "your-super-secret-key"
DB_PATH = Path(__file__).with_name("users.db")

# ---------- DB Helpers ----------

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password_sha256(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()
# ---------- Routes ----------

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        form = request.form
        required_fields = ['first_name', 'last_name', 'user_id', 'username',
                           'password', 'cc_number', 'cc_valid', 'cvc']

        if not all(form.get(field, '').strip() for field in required_fields):
            flash("❌ All fields are required.", "error")
            return render_template('signup.html')

        try:
            user = {
                'first_name': form['first_name'].strip(),
                'last_name': form['last_name'].strip(),
                'user_id': form['user_id'].strip(),
                'username': form['username'].strip(),
                'password': hash_password_sha256(form['password']),
                'cc_number': form['cc_number'].replace(" ", ""),
                'cc_valid': form['cc_valid'],
                'cvc': form['cvc'],
                'is_admin': 0
            }

            with get_db() as db:
                db.execute("""
                    INSERT INTO users (first_name, last_name, user_id, username, password,
                                       cc_number, cc_valid, cvc, is_admin)
                    VALUES (:first_name, :last_name, :user_id, :username, :password,
                            :cc_number, :cc_valid, :cvc, :is_admin)
                """, user)

            flash("✅ User registered successfully!", "success")
            return render_template('success.html')

        except sqlite3.IntegrityError:
            flash("❌ Username or User ID already exists.", "error")
            return render_template('signup.html')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve and strip username and password from the form
        username = request.form['username'].strip()
        password = request.form['password']

        with get_db() as db:
            user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user and hash_password_sha256(user['password'], password):
            role = "admin" if user["is_admin"] else "user"
            msg = f"✅ Welcome <b>{user['username']}</b>! You’re logged in as <b>{role}</b>."
            flash("✅ User logged in successfully!", "success")
            return render_template('success.html')
        else:
            flash("❌ Invalid username or password.", "error")
            return render_template('login.html')
    # Render the login page for GET requests
    return render_template('login.html')

@app.route('/success')
def success():
    return render_template('success.html')
# ---------- Run ----------

if __name__ == '__main__':
    app.run(debug=True)
