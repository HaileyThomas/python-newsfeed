import sys
from flask import Blueprint, request, jsonify, session
from app.models import User
from app.db import get_db

bp = Blueprint("api", __name__, url_prefix="/api")

# create signup api route


@bp.route("/users", methods=["POST"])
def signup():
    data = request.get_json()
    db = get_db()

    try:
        # create a new user
        newUser = User(
            username=data["username"],
            email=data["email"],
            password=data["password"]
        )

        # save in database
        db.add(newUser)
        db.commit()
    except:
        # insert failed, so send error to front end
        db.rollback()
        return jsonify(message="Signup failed"), 500

    # clears any existing session data and creates new session properties
    session.clear()
    # aids in future database queries
    session["user_id"] = newUser.id
    # boolean for templates to use to conditionally render elements
    session["loggedIn"] = True

    return jsonify(id=newUser.id)


@bp.route("/users/login", methods=["POST"])
def login():
    data = request.get_json()
    db = get_db()

    try:
        user = db.query(User).filter(User.email == data["email"]).one()
    except:
        print(sys.exc_info()[0])

    if user.verify_password(data["password"]) == False:
        return jsonify(message="incorrect credentials"), 400

    # if email and password pass the checks, create session and log in
    session.clear()
    session["user_id"] = user.id
    session["loggedIn"] = True

    return jsonify(id=user.id)


@bp.route("/users/logout", methods=["POST"])
def logout():
    # remove session variables
    session.clear()
    return "", 204
