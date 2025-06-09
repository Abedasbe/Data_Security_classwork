from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3, hashlib, re
from pathlib import Path

app = Flask(__name__)
app.secret_key = "replace‑with‑env‑secret"
DB_PATH = Path(__file__).with_name("users.db")


# ───── helpers ─────
def get_db() -> sqlite3.Connection:
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


ILLEGAL = re.compile(r"[\'\";#\-]")  # basic assignment filter


def safe(txt: str) -> bool: return not ILLEGAL.search(txt)


# ───── routes ─────
@app.route("/")
def index(): return redirect(url_for("home"))


@app.route("/home")
def home():  return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        f = request.form
        need = ("first_name last_name user_id username password "
                "cc_number cc_valid cvc").split()
        if not all(f.get(x, "").strip() for x in need):
            flash("❌ All fields required.", "error")
            return render_template("signup.html")

        if not (safe(f["username"]) and safe(f["password"])):
            flash("❌ Username or password has illegal chars.", "error")
            return render_template("signup.html")

        user = {k: f[k].strip() for k in need}
        user["password"] = sha256(user["password"])
        user["cc_number"] = user["cc_number"].replace(" ", "")
        user["is_admin"] = 0

        try:
            with get_db() as db:
                db.execute("""INSERT INTO users
                    (first_name,last_name,user_id,username,password,
                     cc_number,cc_valid,cvc,is_admin)
                    VALUES (:first_name,:last_name,:user_id,:username,:password,
                            :cc_number,:cc_valid,:cvc,:is_admin)""", user)
            return render_template("success.html")
        except sqlite3.IntegrityError:
            return render_template("fail.html")
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"].strip()
        p = request.form["password"]
        if not (safe(u) and safe(p)):
            return render_template("fail.html")

        with get_db() as db:
            row = db.execute("SELECT * FROM users WHERE username = ?", (u,)).fetchone()

        if row and row["password"] == sha256(p):
            role = "admin" if row["is_admin"] else "user"
            return render_template("success.html")

        return render_template("fail.html")
    return render_template("login.html")

@app.route("/success")
def success(): return render_template("success.html")

@app.route("/fail")
def fail(): return render_template("fail.html")

if __name__ == "__main__":
    DB_PATH.touch(exist_ok=True)
    app.run(debug=True)
