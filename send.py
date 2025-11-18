import requests

PAGE_ACCESS_TOKEN = "..."

# Hàm tùy chọn để gửi tin nhắn phản hồi
def send_message(recipient_id, message_text):
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    }
    # Gửi yêu cầu POST đến Messenger API
    response = requests.post("https://graph.facebook.com/v18.0/me/messages", 
                             params=params, headers=headers, json=data)
    if response.status_code != 200:
        print(f"Lỗi gửi tin nhắn: {response.text}")
    else:
        print("Gửi tin nhắn thành công!")

send_message(recipient_id="32402074859406008",message_text="Hello world!")