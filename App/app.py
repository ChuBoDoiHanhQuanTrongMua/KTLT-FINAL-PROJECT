from flask import Flask, render_template, session, redirect, url_for, abort
from login import login_bp
from register import register_bp
from profile import profile_bp
from chat_AI.routes import chat_ai_bp
import os
from tracking import update_learning_progress

# Định nghĩa các nhân vật được chuyển vào một file riêng
from config import CHARACTERS

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(chat_ai_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mainscreen')
def mainscreen():
    return render_template('mainscreen.html')

@app.route('/class')
def class_page():
    # Kiểm tra đăng nhập trước khi truy cập lớp học
    if 'user' not in session:
        return redirect(url_for('login.get_login_page'))
    
    # Cập nhật tiến độ học tập
    username = session['user'].get('username')
    if username:
        update_learning_progress(username, "Class")
    
    return render_template('Class.html')

@app.route('/class/<character>')
def class_character(character):
    """
    Route động cho tất cả các lớp học nhân vật lịch sử
    """
    # Kiểm tra tên nhân vật hợp lệ
    if character not in CHARACTERS:
        abort(404)
    
    # Kiểm tra đăng nhập trước khi truy cập lớp học
    if 'user' not in session:
        return redirect(url_for('login.get_login_page'))
    
    # Cập nhật tiến độ học tập
    username = session['user'].get('username')
    if username:
        update_learning_progress(username, character)
    
    return render_template(f'Class{character}.html')

if __name__ == "__main__":
    app.run(debug=True)
