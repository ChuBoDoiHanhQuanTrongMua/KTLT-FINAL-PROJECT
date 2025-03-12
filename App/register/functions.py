from database import JSON_PATH
import os
import json
from profile.functions import load_users, save_users


def save_to_json(full_name, username, email, phone_number, dob, password):
    """
    Lưu thông tin đăng ký người dùng và tạo các trường mở rộng là null
    cho phần thông tin profile
    """
    users = load_users()

    for user in users:
        if user['username'] == username:
            raise ValueError("User has already been registered.!")

    # Tạo user mới với các trường cơ bản từ trang register
    new_user = {
        "full_name": full_name,
        "username": username,
        "email": email,
        "phone_number": phone_number,
        "dob": dob,
        "password": password,
        # Các trường mở rộng cho profile
        "age": None,
        "gender": None,
        "student_id": None,
        "profile_picture": None,
        "conversation_history": [],
        "classes_attended": [],
        "learning_progress": 0
    }

    users.append(new_user)
    save_users(users)
    return new_user