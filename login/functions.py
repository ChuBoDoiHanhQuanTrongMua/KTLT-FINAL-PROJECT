from database import JSON_PATH
import os
import json

def check_user(username, password):
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = []

    if len(users) == 0:
        return [False, "Lỗi database"]

    for user in users:
        if user["username"] == username and user["password"] == password:
            return [True, f"Hello {user["username"]}"]