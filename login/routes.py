from flask import render_template, request, redirect, url_for, Flask, jsonify
from . import login_bp
from login.functions import check_user

@login_bp.route('/login', methods=['GET'])
def get_login_page():
    return render_template('login.html')

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    status, message = check_user(username, password)

    return jsonify({"status": status, "message": message}), (200 if status else 401)
