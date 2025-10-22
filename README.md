##### Mô tả dự án

Phần mềm lọc tài khoản ảo, mạng xã hội

Ý tưởng hoạt động:

- Chỉ thuần qua tin nhắn
- Kết hợp thêm với ảnh

Đầu vào của người dùng là:

- Tin nhắn dạng văn bản hình ảnh?
- Tin nhắn nhận được từ Fanpage Facebook

Mong muốn:
Có một hệ CSDL chứa đặc điểm nhận dạng lừa đảo
Khi người dùng nhập thông tin, có cơ chế để cập nhật CSDL ở đây

Tổ chức dùng Database?

### Công nghệ sử dụng

- Dùng llama_index xây dựng kết hợp Gemini API cho phát hiện lừa đảo
- Dùng GradIO để dựng giao diện Web tương tác trực tiếp
- Còn cài đặt kết hợp Facebook API để kết nối với Fanpage để nhận tin nhắn

#### Một số cái có thể làm thêm

- Deploy lên Cloud (hiện tại dự án sẽ dùng phần mềm thứ 3, ngrok để tạo tunnel public ra ngoài)
- Thêm phần cập nhật thêm dữ liệu lừa đảo từ Admin
