"""
Module quản lý lớp học và tương tác với người dùng
Chứa các API và routes để hiển thị lớp học, bài giảng và xử lý câu hỏi
"""

from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from historical_character.character_lecture import lectures
from tracking import update_learning_progress, add_conversation_history
import requests
import json
import os
from config import CHARACTERS

# Tạo Blueprint cho classroom
classroom_bp = Blueprint('classroom', __name__, url_prefix='/classroom')

# API key cho Gemini (sẽ sử dụng cho hỏi đáp)
api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyAVQL6DsAB69uPQ_G8LIMlwDwsF56avZEI")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

headers = {
    "Content-Type": "application/json"
}

@classroom_bp.route('/')
def classroom_main():
    """
    Trang chính cho lớp học
    Hiển thị giao diện lớp học tổng quát
    """
    # Kiểm tra đăng nhập
    if 'user' not in session:
        return redirect(url_for('login.get_login_page'))
    
    # Cập nhật tiến độ học tập
    username = session['user'].get('username')
    if username:
        update_learning_progress(username, "Class")
    
    return render_template('Class.html')

@classroom_bp.route('/<character>')
def classroom_character(character):
    """
    Lớp học cho một nhân vật cụ thể
    
    Args:
        character (str): Tên nhân vật muốn học
    
    Returns:
        Template HTML với dữ liệu của nhân vật
    """
    # Kiểm tra tên nhân vật hợp lệ
    if character not in CHARACTERS:
        return jsonify({"error": "Character not found"}), 404
    
    # Kiểm tra đăng nhập
    if 'user' not in session:
        return redirect(url_for('login.get_login_page'))
    
    # Cập nhật tiến độ học tập
    username = session['user'].get('username')
    if username:
        update_learning_progress(username, character)
    
    # Trả về template với dữ liệu nhân vật
    return render_template(f'Class{character}.html')

@classroom_bp.route('/lectures', methods=['GET'])
def get_lectures():
    """
    API lấy nội dung bài giảng cho nhân vật cụ thể
    
    Query Params:
        character (str): Tên nhân vật cần lấy bài giảng
    
    Returns:
        JSON chứa dữ liệu bài giảng của nhân vật
    """
    character_name = request.args.get('character')
    if character_name in lectures:
        return jsonify({"lectures": lectures[character_name]}), 200
    else:
        return jsonify({"error": "Lectures not found for the character."}), 404

@classroom_bp.route('/ask', methods=['POST'])
def ask_question():
    """
    API trả lời câu hỏi của người dùng
    
    JSON Body:
        character (str): Tên nhân vật trả lời câu hỏi
        question (str): Nội dung câu hỏi
    
    Returns:
        JSON chứa câu trả lời từ API Gemini
    """
    # Kiểm tra đăng nhập
    if 'user' not in session:
        return jsonify({"error": "User not logged in"}), 401
    
    # Lấy dữ liệu từ request
    data = request.get_json()
    character_name = data.get('character')
    question = data.get('question')
    
    if not character_name or not question:
        return jsonify({"error": "Missing character or question"}), 400
    
    # Lấy thông tin nhân vật từ lectures
    character_info = ""
    if character_name in lectures:
        for lecture in lectures[character_name]:
            character_info += " ".join(lecture["content"]) + " "
    else:
        return jsonify({"error": "Character not found"}), 404
    
    # Tạo prompt cho API
    content = f"""Bạn là {character_name}, một nhân vật lịch sử. 
    Dưới đây là một số thông tin về bạn:
    {character_info}
    
    Hãy trả lời câu hỏi sau đây với phong cách và kiến thức của {character_name}, 
    nói chuyện ở ngôi thứ nhất như thể bạn là {character_name}. 
    Câu trả lời nên ngắn gọn và súc tích, trong khoảng 1-5 câu.
    
    Câu hỏi: {question}
    """
    
    # Chuẩn bị dữ liệu cho API
    api_data = {
        "contents": [{
            "parts": [{"text": content}]
        }]
    }
    
    try:
        # Gọi API
        response = requests.post(url, headers=headers, data=json.dumps(api_data))
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