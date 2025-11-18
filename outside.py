from flask import Flask, request, jsonify

# Khai báo ứng dụng Flask
app = Flask(__name__)

# Đặt Mã Xác Minh (Verify Token) và Access Token của Trang
# LƯU Ý: Thay thế bằng token của bạn. Nên dùng biến môi trường để bảo mật.
VERIFY_TOKEN = "..." # Đặt một chuỗi bất kỳ, phải trùng với chuỗi nhập trên Facebook Developer
PAGE_ACCESS_TOKEN = "..." # Token truy cập trang

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    # Facebook sẽ gửi yêu cầu GET để xác minh URL
    # Kiểm tra xem các tham số bắt buộc có tồn tại không
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode and token:
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            # Xác minh thành công, trả về hub.challenge
            print("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            # Token không khớp
            return "Verification token mismatch", 403
    return "Missing parameters", 400

@app.route('/webhook', methods=['POST'])
def handle_messages():
    # Facebook sẽ gửi yêu cầu POST khi có sự kiện (ví dụ: người dùng gửi tin nhắn)
    data = request.get_json()
    
    # In dữ liệu nhận được để dễ debug
    print("Dữ liệu nhận được từ webhook:", data)

    # Xử lý sự kiện Messenger
    if data and data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry.get('messaging', []):
                if messaging_event.get('message'):
                    # Lấy ID người gửi và nội dung tin nhắn
                    sender_id = messaging_event['sender']['id']
                    message_text = messaging_event['message']['text']
                    
                    print(f"Tin nhắn từ {sender_id}: {message_text}")
                    
                    # **********************************************
                    # Thêm logic xử lý tin nhắn và gửi phản hồi tại đây
                    # **********************************************
                    # Ví dụ: send_message(sender_id, "Bạn vừa gửi: " + message_text)
                    pass

    return "OK", 200

if __name__ == '__main__':
    # Flask mặc định chạy trên cổng 5000
    app.run(port=5000)