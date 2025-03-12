from database import JSON_PATH
import os
import json

def check_user(username, password):
    """
    Kiểm tra thông tin đăng nhập của người dùng
    Trả về: [status, message]
    - status: True nếu đăng nhập thành công, False nếu thất bại
    - message: Thông báo kết quả
    """
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = []

    if len(users) == 0:
        return [False, "Lỗi database: Không tìm thấy dữ liệu người dùng"]

    for user in users:
        if user["username"] == username and user["password"] == password:
            return [True, f"Xin chào {user['full_name']}!"]
    
    # Nếu không tìm thấy người dùng hoặc mật khẩu không đúng
    return [False, "Tên đăng nhập hoặc mật khẩu không đúng"]