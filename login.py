from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = "secret key"
DB_PATH = 'users.db'


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def get_user(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            # Check if all required fields are present
            required_fields = ['first_name', 'last_name', 'user_id', 'username',
                               'password', 'cc_number', 'cc_valid', 'cvc']

            for field in required_fields:
                print(f"{field}: {field in request.form}")

            missing_fields = [field for field in required_fields if field not in request.form]
            if missing_fields:
                return f"❌ Missing required fields: {', '.join(missing_fields)}", 400

            try:
                first_name = request.form['first_name'].strip()
                last_name = request.form['last_name'].strip()
                user_id = request.form['user_id'].strip()
                username = request.form['username'].strip()
                password = request.form['password']
                cc_number = request.form['cc_number'].strip()
                cc_valid = request.form['cc_valid'].strip()
                cvc = request.form['cvc'].strip()
            except KeyError as e:
                return f"❌ Failed to get field: {str(e)}", 400

            # Validate empty fields
            if not all([first_name, last_name, user_id, username, password, cc_number, cc_valid, cvc]):
                return "❌ All fields must be filled out", 400

            # For debugging - print received data (remove in production)
            print("Received form data:", {
                'first_name': first_name,
                'last_name': last_name,
                'user_id': user_id,
                'username': username,
                'cc_number': cc_number,
                'cc_valid': cc_valid,
                'cvc': cvc
            })

            hashed = hash_password(password)

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    first_name TEXT,
                    last_name TEXT,
                    user_id TEXT UNIQUE,
                    username TEXT UNIQUE,
                    password TEXT,
                    cc_number TEXT,
                    cc_valid TEXT,
                    cvc TEXT,
                    is_admin INTEGER DEFAULT 0
                )
            """)

            cursor.execute("""
                INSERT INTO users (first_name, last_name, user_id, username, password, 
                                 cc_number, cc_valid, cvc, is_admin)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (first_name, last_name, user_id, username, hashed,
                  cc_number, cc_valid, cvc, 0))
            
            conn.commit()
            msg = "✅ User registered successfully!"
            
        except sqlite3.OperationalError as e:
            msg = f"❌ Database Error: {str(e)}"
            print("Database Error:", str(e))
            return msg, 500
        except sqlite3.IntegrityError as e:
            msg = f"❌ Data Error: Username or User ID already exists"
            print("Integrity Error:", str(e))
            return msg, 400
        except Exception as e:
            msg = f"❌ Unexpected Error: {str(e)}"
            print("Unexpected Error:", str(e))
            return msg, 500
        finally:
            if 'conn' in locals():
                conn.close()
            
        return render_template('success.html', message=msg)
    
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed = hash_password(password)
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashed}'"

        print("Executing SQL:", query)

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            user = cursor.execute(query).fetchone()
        except sqlite3.OperationalError as e:
            return f"SQL Error: {e}"

        if user:
            return f"✅ Welcome {user['username']}! Your role: {user['role']}"
        else:
            return "❌ Log in failed."
    return render_template('login.html')

@app.route('/forgot')
def forgot_password():
    return "Password reset is not possible. Contact admin."

# Add this route
@app.route('/')
def index():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
