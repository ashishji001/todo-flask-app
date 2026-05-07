from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = "dev-secret-key-change-me"  # replace in production

db = SQLAlchemy(app)


# -------------------------
# Models
# -------------------------
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)


# # Create tables
# with app.app_context():
#     db.create_all()


# -------------------------
# Auth helpers
# -------------------------
def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)


# -------------------------
# Routes - Tasks
# -------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        task_content = (request.form.get("task") or "").strip()
        if task_content:
            db.session.add(Todo(task=task_content))
            db.session.commit()
        return redirect(url_for("home"))

    tasks = Todo.query.all()
    return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    task = Todo.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    task = Todo.query.get_or_404(id)

    if request.method == "POST":
        new_text = (request.form.get("task") or "").strip()
        if not new_text:
            return render_template("edit_task.html", todo=task, error="Task cannot be empty.")

        task.task = new_text
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit_task.html", todo=task)


# -------------------------
# Routes - Auth
# -------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        if not name or not email or not password:
            return render_template("signup.html", error="All fields are required.")

        if User.query.filter_by(email=email).first():
            return render_template("signup.html", error="Email already registered.")

        user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
        )
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        return redirect(url_for("home"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return render_template("login.html", error="Invalid email or password.")

        session["user_id"] = user.id
        return redirect(url_for("home"))

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    return render_template("profile.html", user=user)

with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(e)

app = app

if __name__ == "__main__":
    app.run()
