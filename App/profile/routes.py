from flask import render_template, request, redirect, url_for, session, jsonify, flash
from . import profile_bp
from profile.functions import update_profile_data, load_users
import os
from werkzeug.utils import secure_filename


@profile_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    # Kiểm tra nếu chưa đăng nhập
    if 'user' not in session:
        return redirect(url_for('login.get_login_page'))

    if request.method == 'GET':
        user_data = session['user']  # Lấy thông tin từ session
        return render_template('profile.html', user=user_data)

    elif request.method == 'POST':
        # Lấy content-type nếu có
        content_type = request.headers.get('Content-Type', '')
        
        # Xử lý khi người dùng bấm nút Save (form thông thường hoặc multipart)
        if 'application/json' not in content_type:
            try:
                # Lấy dữ liệu từ form
                updated_data = {
                    'full_name': request.form.get('name'),
                    'email': request.form.get('email'),
                    'phone_number': request.form.get('phone'),
                    'age': request.form.get('age'),
                    'gender': request.form.get('gender'),
                    'student_id': request.form.get('student-id')
                }
                
                # Xử lý tải lên ảnh đại diện nếu có
                if 'profile-picture' in request.files:
                    profile_pic = request.files['profile-picture']
                    if profile_pic and profile_pic.filename != '':
                        # Lưu file ảnh
                        filename = secure_filename(profile_pic.filename)
                        # Tạo thư mục uploads nếu chưa có
                        upload_folder = os.path.join('static', 'uploads')
                        os.makedirs(upload_folder, exist_ok=True)
                        
                        file_path = os.path.join(upload_folder, filename)
                        profile_pic.save(file_path)
                        
                        # Cập nhật đường dẫn ảnh vào dữ liệu người dùng
                        updated_data['profile_picture'] = '/' + file_path.replace('\\', '/')
                
                username = session['user'].get("username")
                
                updated_user = update_profile_data(username, updated_data)
                # Cập nhật session với thông tin mới
                session['user'] = updated_user
                flash('Profile updated successfully!', 'success')
                return redirect(url_for('profile.profile'))
            except ValueError as ve:
                flash(str(ve), 'error')
                return redirect(url_for('profile.profile'))
            except Exception as e:
                flash(f"Lỗi không xác định: {str(e)}", 'error')
                return redirect(url_for('profile.profile'))
        
        # Xử lý AJAX request (json)
        else:
            try:
                data = request.get_json()
                if data is None:
                    return jsonify({"status": False, "message": "Dữ liệu không hợp lệ"}), 400
                    
                username = session['user'].get("username")
                if not username:
                    return jsonify({"status": False, "message": "User not found in session"}), 401

                updated_user = update_profile_data(username, data)
                # Cập nhật session
                session['user'] = updated_user
                return jsonify({"status": True, "message": "Profile updated successfully"}), 200
            except ValueError as ve:
                return jsonify({"status": False, "message": str(ve)}), 404
            except Exception as e:
                return jsonify({"status": False, "message": f"Lỗi không xác định: {str(e)}"}), 500

