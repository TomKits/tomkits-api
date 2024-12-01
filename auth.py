from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    current_user,
    get_jwt_identity,
)
from models import User, TokenBlocklist

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register_user():
    data = request.get_json()

    # Validasi panjang password
    password = data.get("password")
    if not password or len(password) < 8:
        return jsonify({"error": "Password must be 8 characters or longer"}), 400

    # Cek apakah user sudah terdaftar
    user = User.get_user_by_email(email=data.get("email"))
    if user is not None:
        return jsonify({"error": "User already exists"}), 409

    # Membuat user baru
    new_user = User(username=data.get("username"), email=data.get("email"))
    new_user.set_password(password=password)
    new_user.save()

    return jsonify({"message": "User Created!"}), 201



@auth_bp.post("/login")
def login_user():

    data = request.get_json()

    user = User.get_user_by_email(email=data.get("email"))

    if user and (user.check_password(password=data.get("password"))):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return (
            jsonify(
                {
                    "message": "You're Logged In ",
                    "token": {"access": access_token, "refresh": refresh_token},
                }
            ),
            200,
        )

    return jsonify({"error": "Invalid Username or Password"}), 400


@auth_bp.get("/whoami")
@jwt_required()
def whoami():
    claims = get_jwt()
    return jsonify(
        {
            "message": "message",
            "user_details": {
                "username": current_user.username,
                "email": current_user.email,
            },
        }
    )


@auth_bp.get("/refresh")
@jwt_required(refresh=True)
def refresh_access():
    identity = get_jwt_identity()

    new_access_token = create_access_token(identity=identity)

    return jsonify({"accestoken": new_access_token})


@auth_bp.get("/logout")
@jwt_required(verify_type=False)
def logout_user():
    jwt = get_jwt()

    jti = jwt["jti"]
    token_type = jwt["type"]

    token_b = TokenBlocklist(jti=jti)
    token_b.save()

    return jsonify({"message": f"{token_type} token revoked successfully"}), 200
