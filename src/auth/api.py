from flask import Blueprint, request, make_response, url_for
from flask_mail import Message
from itsdangerous import URLSafeSerializer
from werkzeug.security import generate_password_hash, check_password_hash

from src.database import get_user_by_email, add_user, update_user, get_user_by_id

auth_api = Blueprint("auth_api", __name__, url_prefix="/oauth")
serializer = URLSafeSerializer("a3f7b6c8d9e10234f5a6b7c8d9e01234f5a6b7c8d9e01234f5a6b7c8d9e01234")


def send_confirmation_email(email):
    from src.factory import mail

    token = serializer.dumps(email, salt="email-confirmation-salt")
    confirm_url = url_for("auth_api.verify_email", token=token, _external=True)

    msg = Message(
        subject='Sustains Email Verification',
        recipients=[email],
        sender="harshahari1642@gmail.com",
        body=f"Click the link to verify your email: {confirm_url}"
    )

    mail.send(msg)


@auth_api.route("/verify-email/<token>", methods=["GET"])
def verify_email(token):
    try:
        email = serializer.loads(token, salt="email-confirmation-salt", max_age=3600)  # Token expires in 1 hour
        # Mark email as verified in the database
        user = get_user_by_email(email=email)
        if user:
            update_user(user=user, update={"verified": True})
            return "Email verified successfully!"
        else:
            return "User not found"
    except:
        return "Invalid or expired token"


@auth_api.route('/register', methods=["POST"])
def api_register_user():
    name = request.json["name"]
    email = request.json["email"]
    password = request.json["password"]

    if not all([name, email, password]):
        response = {
            "success": False,
            "message": "email, password and name are required."
        }
        return make_response(response, 400)

    user = get_user_by_email(email=email)

    if user:
        if not user.get('verified', False):
            response = {
                "success": False,
                "message": "Email already registered but not verified. A verification link has been sent to your email id."
            }
            send_confirmation_email(email)
        else:
            response = {
                "success": False,
                "message": "Email already registered. Please log in or use a different email."
            }
        return make_response(response, 400)

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    new_user = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "verified": False
    }

    add_user(user=new_user)

    # Send the confirmation email
    send_confirmation_email(email)

    response = {
        "success": True,
        "message": "A verification link has been sent to your email id"
    }

    return make_response(response, 200)


@auth_api.route('/login', methods=["POST"])
def api_login_user():
    email = request.json["email"]
    password = request.json["password"]

    if not email or not password:
        response = {
            "success": False,
            "message": "email and password are required."
        }
        return make_response(response, 400)

    user = get_user_by_email(email=email)

    if not user:
        response = {
            "success": False,
            "message": "Invalid email or password"
        }
        return make_response(response, 404)

    if not check_password_hash(user["password"], password):
        response = {
            "success": False,
            "message": "Invalid email or password"
        }
        return make_response(response, 404)

    if not user.get('verified', False):
        response = {
            "success": False,
            "message": "Email is not verified. A verification link has been sent to your email id."
        }
        send_confirmation_email(email=email)
        return make_response(response, 400)

    response = {
        "success": True,
        "id": str(user["_id"])
    }

    return make_response(response, 200)


@auth_api.route('/user/<string:id>', methods=["GET"])
def api_user_details(id):
    user = get_user_by_id(id=id)
    if not user:
        response = {
            "success": False,
            "message": "User not found"
        }
        return make_response(response, 404)

    response = {
        "success": True,
        "id": id,
        "name": user["name"],
        "email": user["email"]
    }

    return make_response(response, 200)
