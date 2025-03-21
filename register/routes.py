from flask import render_template, request, redirect, url_for, Flask, jsonify
from . import register_bp
from register.functions import save_to_json

@register_bp.route('/register', methods=['GET'])
def get_register_page():
    return render_template("register.html")


@register_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    full_name = data.get('full_name')
    username = data.get('username')
    email = data.get('email')
    phone_number = data.get('phone_number')
    dob = data.get('dob')
    password = data.get('password')

    # SAVE USER
    try:
        save_to_json(full_name, username, email, phone_number, dob, password)
    except ValueError as ve:
        print("HERE")
        return jsonify({"status": False, "message": str(ve)}), 400

    return jsonify({"status": True, "message": "Register successful"}), 201
