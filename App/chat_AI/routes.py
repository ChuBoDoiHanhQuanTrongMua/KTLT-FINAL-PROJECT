from flask import Blueprint, request, jsonify, session, redirect, url_for
from historical_character.introduction import characters
import requests
import json
from historical_character.character_lecture import lectures
from tracking import add_conversation_history
import os
from . import chat_ai_bp

# Lấy API key từ biến môi trường, hoặc sử dụng giá trị mặc định nếu không có
api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyAVQL6DsAB69uPQ_G8LIMlwDwsF56avZEI")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

headers = {
    "Content-Type": "application/json"
}

@chat_ai_bp.route('/ask', methods=['POST'])
def ask_character():
    # Kiểm tra đăng nhập trước khi xử lý yêu cầu
    if 'user' not in session:
        return jsonify({"error": "User not logged in"}), 401
    
    data = request.get_json()
    character_name = data.get('character')
    question = data.get('question')

    # Tìm phần giới thiệu của nhân vật
    introduction = None
    for category, chars in characters.items():
        if character_name in chars:
            introduction = chars[character_name]
            break

    if not introduction:
        return jsonify({"error": "Character not found."}), 404

    # Tạo nội dung cho API
    content = f"Bạn là {character_name}. Đây là một số thông tin về bạn: {introduction}\n\nHãy trả lời câu hỏi sau một cách ngắn gọn nhất có thể với phong cách và kiến thức của {character_name}, nói chuyện ở ngôi thứ nhất như thể bạn là {character_name}. Câu hỏi: {question}"
    data = {
        "contents": [{
            "parts": [{"text": content}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()

        result = response.json()
        if 'candidates' in result and result['candidates']:
            answer = result['candidates'][0]['content']['parts'][0]['text']
            
            # Lưu lịch sử hội thoại
            username = session['user'].get('username')
            if username:
                add_conversation_history(username, character_name, question, answer)
            
            return jsonify({"answer": answer})
        else:
            return jsonify({"error": "No candidates found in the response."}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error calling API: {e}"}), 500
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Error decoding JSON response: {e}"}), 500
    except KeyError as e:
        return jsonify({"error": f"Error accessing key in JSON response: {e}"}), 500

@chat_ai_bp.route('/lectures', methods=['GET'])
def get_lectures():
    character_name = request.args.get('character')
    if character_name in lectures:
        return jsonify({"lectures": lectures[character_name]}), 200
    else:
        return jsonify({"error": "Lectures not found for the character."}), 404