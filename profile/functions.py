from database import JSON_PATH
import json
import os

def load_users():
    """Load users from JSON file."""
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as file:
            users = json.load(file)
        return users
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_users(users):
    """Save users to JSON file."""
    os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)
    with open(JSON_PATH, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4, ensure_ascii=False)

def update_profile_data(username, updated_data):
    """Update existing user profile with new data."""
    users = load_users()

    for user in users:
        if user["username"] == username:
            # Cập nhật tất cả các trường dữ liệu từ form
            for key, value in updated_data.items():
                user[key] = value
            
            save_users(users)
            return user  # Trả về user đã cập nhật
            
    raise ValueError("User not found!")