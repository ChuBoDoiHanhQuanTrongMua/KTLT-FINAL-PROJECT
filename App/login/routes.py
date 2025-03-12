from flask import render_template, request, redirect, url_for, Flask, jsonify, session
from . import login_bp
from login.functions import check_user
from profile.functions import load_users

@login_bp.route('/login', methods=['GET'])
def get_login_page():
    return render_template('login.html')

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    status, message = check_user(username, password)
    
    if status:
        # Lưu thông tin người dùng vào session khi đăng nhập thành công
        users = load_users()
        for user in users:
            if user["username"] == username:
                session['user'] = user
                break

    return jsonify({"status": status, "message": message}), (200 if status else 401)

@login_bp.route('/logout')
def logout():
    # Xóa thông tin người dùng khỏi session
    session.pop('user', None)
    return redirect(url_for('login.get_login_page'))
