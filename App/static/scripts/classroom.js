// Classroom script for handling lectures and interaction
document.addEventListener('DOMContentLoaded', function() {
    // Lấy tên nhân vật từ thuộc tính data
    const characterName = document.getElementById('lecture-title').dataset.character;
    
    // Khai báo biến toàn cục
    let lectureContents = [];
    let currentLectureIndex = 0;
    let currentLineIndex = 0;
    const lectureContent = document.getElementById('lecture-content');
    const chalkPiece = document.getElementById('chalk-piece');
    const chalkDustContainer = document.getElementById('chalk-dust-container');
    const blackboard = document.querySelector('.blackboard');
    let autoScrollEnabled = true;
    
    // Thêm nút chuyển đổi tự động cuộn
    const scrollToggleBtn = document.createElement('button');
    scrollToggleBtn.className = 'scroll-toggle-btn';
    scrollToggleBtn.textContent = 'Tự động cuộn: Bật';
    scrollToggleBtn.style.position = 'absolute';
    scrollToggleBtn.style.right = '10px';
    scrollToggleBtn.style.top = '5px';
    scrollToggleBtn.style.fontSize = '12px';
    scrollToggleBtn.style.padding = '2px 5px';
    scrollToggleBtn.style.background = 'rgba(255, 255, 255, 0.2)';
    scrollToggleBtn.style.color = 'white';
    scrollToggleBtn.style.border = 'none';
    scrollToggleBtn.style.borderRadius = '3px';
    scrollToggleBtn.style.cursor = 'pointer';
    scrollToggleBtn.style.zIndex = '5';
    blackboard.appendChild(scrollToggleBtn);
    
    scrollToggleBtn.addEventListener('click', function() {
        autoScrollEnabled = !autoScrollEnabled;
        this.textContent = autoScrollEnabled ? 'Tự động cuộn: Bật' : 'Tự động cuộn: Tắt';
    });
    
    // Lấy nội dung bài giảng từ server
    fetch(`/lectures?character=${characterName}`)
        .then(response => response.json())
        .then(data => {
            console.log("API Response data:", data);
            if (data.lectures) {
                // Sử dụng dữ liệu từ API
                lectureContents = data.lectures;
                currentLectureIndex = 0;
                currentLineIndex = 0;
                lectureContent.innerHTML = '';
                // Bắt đầu hiển thị nội dung
                setTimeout(writeLine, 1000);
            }
        })
        .catch(error => {
            console.error("Fetch error:", error);
        });

    function createChalkDust(x, y) {
        for (let i = 0; i < 5; i++) {
            const dust = document.createElement('div');
            dust.className = 'chalk-dust';
            dust.style.left = (x + Math.random() * 10 - 5) + 'px';
            dust.style.top = (y + Math.random() * 10 - 5) + 'px';
            chalkDustContainer.appendChild(dust);

            setTimeout(() => dust.remove(), 1200);
        }
    }

    function moveChalkTo(x, y) {
        // Lưu vị trí cuộn hiện tại
        const currentScrollTop = blackboard.scrollTop;
        
        // Điều chỉnh vị trí Y khi cuộn xuống
        const adjustedY = y - blackboard.scrollTop;
        
        chalkPiece.style.left = x + 'px';
        chalkPiece.style.top = adjustedY + 'px';
        createChalkDust(x, adjustedY);
        
        // Không thay đổi vị trí cuộn
        blackboard.scrollTop = currentScrollTop;
    }

    function writeLine() {
        if (!lectureContents || lectureContents.length === 0) {
            return; // Tránh lỗi nếu dữ liệu chưa được tải
        }
        
        // Lưu vị trí cuộn hiện tại
        const currentScrollTop = blackboard.scrollTop;
        
        // Nếu đã hiển thị hết nội dung của lecture hiện tại
        if (currentLineIndex >= lectureContents[currentLectureIndex].content.length) {
            // Nếu còn lecture tiếp theo thì chuyển sang lecture tiếp theo
            if (currentLectureIndex < lectureContents.length - 1) {
                setTimeout(() => {
                    currentLectureIndex++;
                    currentLineIndex = 0;
                    lectureContent.innerHTML = '';
                    writeLine();
                }, 5000);
            } else {
                // Đã hiển thị hết tất cả nội dung, không lặp lại
                console.log("Đã hiển thị hết tất cả nội dung của nhân vật.");
            }
            return;
        }

        const line = lectureContents[currentLectureIndex].content[currentLineIndex];
        const lineElement = document.createElement('div');
        lineElement.style.marginBottom = '10px'; // Thêm khoảng cách giữa các dòng

        if (currentLineIndex === 0) {
            lineElement.innerHTML = `<h3 class="writing-text title-text">${line}</h3>`;
        } else if (line.includes('=')) {
            lineElement.innerHTML = `<div class="writing-text formula-text">${line}</div>`;
        } else {
            lineElement.innerHTML = `<p class="writing-text normal-text">${line}</p>`;
        }

        lectureContent.appendChild(lineElement);

        // Tự động cuộn xuống nếu được bật và nội dung đã vượt quá khung nhìn
        if (autoScrollEnabled && 
            lectureContent.offsetHeight > blackboard.offsetHeight && 
            currentLineIndex > 3) { // Chỉ tự động cuộn sau vài dòng
            blackboard.scrollTop = lectureContent.offsetHeight - blackboard.offsetHeight + 50;
        }

        const blackboardRect = blackboard.getBoundingClientRect();
        const startX = blackboardRect.left + (blackboardRect.width * 0.25);
        const startY = blackboardRect.top + (blackboardRect.height * 0.1) + (currentLineIndex * 35);

        moveChalkTo(startX, startY);

        let currentCharIndex = 0;
        const textLength = line.length;

        function animateWriting() {
            if (currentCharIndex < textLength) {
                const progress = currentCharIndex / textLength;
                const x = startX + (blackboardRect.width * 0.5 * progress);
                moveChalkTo(x, startY);

                currentCharIndex++;
                setTimeout(animateWriting, 50);
            } else {
                currentLineIndex++;
                setTimeout(writeLine, 1000);
            }
        }

        animateWriting();
    }

    // Thêm event listener cho thanh cuộn
    blackboard.addEventListener('scroll', function() {
        // Cập nhật vị trí phấn theo thanh cuộn
        const blackboardRect = blackboard.getBoundingClientRect();
        const y = blackboardRect.top + (blackboardRect.height * 0.1) + (currentLineIndex * 35);
        moveChalkTo(chalkPiece.offsetLeft, y);
    });

    function updateHandPosition() {
        const blackboardRect = blackboard.getBoundingClientRect();
        const hand = document.querySelector('.teacher-hand');
        if (!hand) return; // Tránh lỗi nếu không có phần tử hand

        // Lấy vị trí hiện tại của dòng đang viết
        let currentY = blackboardRect.top + (blackboardRect.height * 0.1) + (currentLineIndex * 35);
        
        // Điều chỉnh vị trí Y khi cuộn xuống
        currentY = currentY - blackboard.scrollTop;
        
        const currentX = blackboardRect.left + (blackboardRect.width * 0.5);

        const teacherRect = document.querySelector('.teacher').getBoundingClientRect();
        const angle = Math.atan2(
            currentY - (teacherRect.top + teacherRect.height * 0.4),
            currentX - (teacherRect.left + teacherRect.width * 0.1)
        ) * 180 / Math.PI;

        if (hand) {
            hand.style.transform = `rotate(${angle}deg)`;
        }
    }

    setInterval(updateHandPosition, 100);

    const blackboardRect = blackboard.getBoundingClientRect();
    chalkPiece.style.left = (blackboardRect.left + blackboardRect.width * 0.25) + 'px';
    chalkPiece.style.top = (blackboardRect.top + blackboardRect.height * 0.1) + 'px';
    
    // Thêm sự kiện cho nút gửi câu hỏi
    document.querySelector('.send-btn').addEventListener('click', function() {
        const chatbox = document.querySelector('.chatbox');
        const question = chatbox.value;
        if (question.trim() === '') return;

        // Xóa nội dung hiện tại trên bảng
        lectureContent.innerHTML = '';
        
        // Hiển thị thông báo đang xử lý
        const processingElement = document.createElement('div');
        processingElement.innerHTML = '<p class="writing-text normal-text">Câu hỏi hay đấy...</p>';
        lectureContent.appendChild(processingElement);

        // Gửi câu hỏi đến API
        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                character: characterName,
                question: question
            })
        })
        .then(response => response.json())
        .then(data => {
            // Xóa thông báo đang xử lý
            lectureContent.innerHTML = '';
            
            if (data.answer) {
                // Hiển thị câu trả lời với hiệu ứng viết
                const answerElement = document.createElement('div');
                answerElement.innerHTML = `<p class="writing-text normal-text">${data.answer}</p>`;
                lectureContent.appendChild(answerElement);
                
                // Tự động cuộn lên đầu
                setTimeout(() => {
                    blackboard.scrollTop = 0;
                }, 100);
                
                // Xóa nội dung chatbox
                chatbox.value = '';
            } else if (data.error) {
                const errorElement = document.createElement('div');
                errorElement.innerHTML = `<p class="writing-text normal-text error-text">Lỗi: ${data.error}</p>`;
                lectureContent.appendChild(errorElement);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            const errorElement = document.createElement('div');
            errorElement.innerHTML = `<p class="writing-text normal-text error-text">Lỗi kết nối đến server</p>`;
            lectureContent.appendChild(errorElement);
        });
    });
    
    // Thêm event listener cho phím Enter trong chatbox
    document.querySelector('.chatbox').addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            document.querySelector('.send-btn').click();
        }
    });
});