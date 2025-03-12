from profile.functions import load_users, save_users
from flask import session
import datetime

# Danh sách tất cả các lớp học có trong hệ thống sẽ được import từ app.py
# Để tránh trùng lặp danh sách, comment lại phần này và import từ app
# ALL_CLASSES = [
#     "Einstein", "Newton", "Curie", "Tesla", "Aristotle", 
#     "KhongTu", "DaVinci", "Shakespeare", "Beethoven", 
#     "Napoleon", "TonTu", "Caesar", "Socrates"
# ]

# Sử dụng import từ config để tránh trùng lặp
from config import CHARACTERS as ALL_CLASSES

TOTAL_CLASSES = len(ALL_CLASSES)

def update_learning_progress(username, character=None):
    """
    Cập nhật tiến độ học tập của người dùng khi họ tham gia lớp học
    Hiển thị dưới dạng X/13 thay vì phần trăm
    """
    users = load_users()

    for user in users:
        if user["username"] == username:
            # Khởi tạo classes_attended nếu chưa có
            if "classes_attended" not in user:
                user["classes_attended"] = []
            
            # Tạo thông tin lớp học đã tham gia
            current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            class_info = f"{character} - {current_time}"
            class_name = class_info.split(' - ')[0]  # Lấy tên nhân vật
            
            # Kiểm tra xem đã có lớp học này chưa (chỉ kiểm tra tên nhân vật)
            already_attended = False
            for attended in user["classes_attended"]:
                if attended.split(' - ')[0] == class_name:
                    already_attended = True
                    break
            
            # Chỉ thêm vào nếu chưa học lớp này trước đó
            if not already_attended:
                user["classes_attended"].append(class_info)
            
            # Tính số lớp đã tham gia (đếm theo tên nhân vật, không trùng lặp)
            attended_classes = set()
            for attended in user["classes_attended"]:
                character_name = attended.split(' - ')[0]
                # Chỉ đếm các lớp học hợp lệ trong danh sách ALL_CLASSES
                if character_name in ALL_CLASSES:
                    attended_classes.add(character_name)
            
            # Cập nhật learning_progress (giới hạn tối đa là số lớp học trong ALL_CLASSES)
            user["learning_progress"] = min(len(attended_classes), len(ALL_CLASSES))
            
            # Cập nhật session
            if 'user' in session:
                session['user'] = user
            
            save_users(users)
            
            return user
    
    return None

def add_conversation_history(username, character, question, answer):
    """
    Thêm lịch sử hội thoại khi người dùng trò chuyện với nhân vật
    """
    users = load_users()

    for user in users:
        if user["username"] == username:
            # Khởi tạo conversation_history nếu chưa có
            if "conversation_history" not in user:
                user["conversation_history"] = []
            
            # Tạo thông tin hội thoại
            current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            conversation = {
                "date": current_time,
                "character": character,
                "content": f"Q: {question}\nA: {answer}"
            }
            
            # Thêm vào lịch sử hội thoại
            user["conversation_history"].append(conversation)
            
            # Giới hạn số lượng hội thoại lưu trữ (tối đa 20)
            if len(user["conversation_history"]) > 20:
                user["conversation_history"] = user["conversation_history"][-20:]
            
            # Cập nhật session
            if 'user' in session:
                session['user'] = user
            
            save_users(users)
            return user
    
    return None 