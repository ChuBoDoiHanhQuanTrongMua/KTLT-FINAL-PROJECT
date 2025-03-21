from flask import Flask, render_template, redirect, url_for
from login import login_bp
from register import register_bp
from profile import profile_bp
from chat_AI.routes import chat_ai_bp
from classroom import classroom_bp
from classroom.routes import *  # Import tất cả từ routes để đăng ký các route
import os
from dotenv import load_dotenv

# Tải các biến môi trường từ tệp .env
load_dotenv()

# Định nghĩa các nhân vật được chuyển vào một file riêng
from config import CHARACTERS

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(chat_ai_bp)
app.register_blueprint(classroom_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mainscreen')
def mainscreen():
    return render_template('mainscreen.html')

# Chuyển hướng đến blueprint classroom
@app.route('/class')
def class_page():
    return redirect(url_for('classroom.classroom_main'))

# Chuyển hướng đến trang lớp học của nhân vật cụ thể
@app.route('/class/<character>')
def class_character(character):
    return redirect(url_for('classroom.classroom_character', character=character))

if __name__ == "__main__":
    app.run(debug=True)
