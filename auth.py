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
from validate import validate_email,validate_password

auth_bp = Blueprint("auth", __name__)


# Endpoint untuk register user
@auth_bp.post("/register")
def register_user():
    data = request.get_json()

    # Inisialisasi peta kesalahan
    errors = {}

    # Validasi password
    password = data.get("password")
    password_errors = validate_password(password)
    if password_errors:
        errors["password"] = password_errors

    # Validasi email
    email = data.get("email")
    email_errors = validate_email(email)
    if email_errors:
        errors["email"] = email_errors

    # Jika ada kesalahan, kembalikan map kesalahan
    if errors:
        return jsonify({"errors": errors}), 400

    # Cek apakah user sudah terdaftar
    user = User.get_user_by_email(email=email)
    if user is not None:
        return jsonify({"error": "User already exists"}), 409

    # Membuat user baru
    new_user = User(username=data.get("username"), email=email)
    new_user.set_password(password=password)
    new_user.save()

    return jsonify({"message": "User Created!"}), 201

# Endpoint untuk login user
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
                    "message": "You're Logged In",
                    "token": {"access": access_token, "refresh": refresh_token},
                }
            ),
            200,
        )

    return jsonify({"error": "Invalid Username or Password"}), 400

# Endpoint untuk menampilkan info user
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

# Endpoint untuk refresh token
@auth_bp.get("/refresh")
@jwt_required(refresh=True)
def refresh_access():
    identity = get_jwt_identity()

    new_access_token = create_access_token(identity=identity)

    return jsonify({"access_token": new_access_token})

# Endpoint untuk logout user
@auth_bp.get("/logout")
@jwt_required(verify_type=False)
def logout_user():
    jwt = get_jwt()

    jti = jwt["jti"]
    token_type = jwt["type"]

    token_b = TokenBlocklist(jti=jti)
    token_b.save()

    return jsonify({"message": f"{token_type} token revoked successfully"}), 200
