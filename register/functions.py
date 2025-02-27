from database import JSON_PATH
import os
import json


def save_to_json(full_name, username, email, phone_number, dob, password):
    os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)

    try:
        with open(JSON_PATH, "r", encoding="utf-8") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = []

    for user in users:
        if user['username'] == username:
            raise ValueError("User has already been registered.!")

    users.append({
        "full_name": full_name,
        "username": username,
        "email": email,
        "phone_number": phone_number,
        "dob": dob,
        "password": password
    })

    with open(JSON_PATH, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4, ensure_ascii=False)