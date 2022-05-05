from flask import Blueprint, render_template

# Blueprint lets us consolidate routes onto a single bp object that the parent app can register later
# like the Router middleware in Express.js
bp = Blueprint("home", __name__, url_prefix="/")

# define home route function


@bp.route("/")
def index():
    return render_template("homepage.html")

# define login route function


@bp.route("/login")
def login():
    return render_template("login.html")

# define post route function


@bp.route("/post/<id>")
def single(id):
    return render_template("single-post.html")
