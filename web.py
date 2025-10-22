import gradio as gr
from chatbot_configure import query_engine, parser

def normalize_response(resp):
    resp = parser.parse(resp.response)
    return resp.model_dump()


# Dữ liệu mẫu sẽ được trả về sau khi "phân tích"
def get_mock_analysis(input_text):
    query = query_engine.query(input_text)
    try :
        query = normalize_response(query)
    except Exception as e:
        query = {
            "CoPhaiLuaDao": "Không xác định",
            "MucDoTuTin": 0,
            "DacDiem": [
            ],
            "GiaiThich": "Lỗi xử lí (có thể do API, mẫu truy vấn)"
        }
    return query

# CSS cho Gradient (Giữ nguyên)
custom_css = custom_css = """
#confidence_slider .wrap-inner .slider-fill {
    /* MỚI: Tăng kích thước nền lên 100% để gradient kéo dài hết chiều rộng */
    background-size: 100% 100% !important; 
    
    /* MỚI: Đặt ảnh nền (gradient) bắt đầu từ mép trái của toàn bộ thanh trượt (vị trí 0) */
    /* background-position: left center; cũng có thể hoạt động */
    
    background-image: linear-gradient(to right, #4CAF50, #FFEB3B, #F44336) !important;
    background-color: transparent !important; 
}

/* Quan trọng: Áp dụng CSS cho toàn bộ container để cố định vị trí gradient */
#confidence_slider .wrap-inner {
    /* Đảm bảo nền của toàn bộ thanh trượt không có màu fill */
    background-color: transparent !important;
}

/* Thêm màu cho phần còn lại của thanh trượt (nếu cần) */
#confidence_slider .wrap-inner .slider-track {
    background-color: #e0e0e0 !important; /* Màu xám nhạt cho phần chưa điền */
}
"""

# --- HÀM XỬ LÝ CHÍNH TRONG GRADIO ---
def analyze_scam(input_text):
    """Hàm xử lý logic và trả về các giá trị đầu ra cho Gradio."""
    if not input_text:
        # Giá trị khởi tạo cho các thành phần
        empty_html = "<p style='color: gray;'>Vui lòng nhập nội dung để phân tích.</p>"
        return "⚠️ VUI LÒNG NHẬP NỘI DUNG", 0, empty_html, "Vui lòng nhập nội dung cần kiểm tra vào ô trên và nhấn 'Phân tích'."

    data = get_mock_analysis(input_text)
    is_scam = data["CoPhaiLuaDao"] == "Có"

    # Chuẩn bị dữ liệu đầu ra
    text_result = "⚠️ PHÁT HIỆN LỪA ĐẢO" if is_scam else "✅ AN TOÀN"
    confidence = data['MucDoTuTin']
    explanation = data["GiaiThich"]

    # 💡 TẠO CHUỖI DANH SÁCH CÓ ĐỊNH DẠNG ĐẸP TỪ MẢNG
    # Sử dụng biểu tượng "🔴" hoặc "🔥" và định dạng HTML/Markdown
    features_list_markdown = ""
    if data['DacDiem']:
        features_list_markdown = "<ul>"
        for d in data['DacDiem']:
            # Dùng biểu tượng và thẻ <li> để tạo danh sách bullet đẹp mắt
            features_list_markdown += f"<li style='margin-bottom: 5px;'> 🛑 &nbsp; <strong>{d}</strong></li>"
        features_list_markdown += "</ul>"
    else:
        features_list_markdown = "Không có đặc điểm nào được phát hiện."

    # Hàm trả về 4 giá trị theo đúng thứ tự của các thành phần đầu ra
    return text_result, confidence, features_list_markdown, explanation


# --- Hàm tạo giao diện Gradio ---
def create_scam_checker_ui():
    
    # Định nghĩa các thành phần Output
    with gr.Blocks(title="Phân tích Lừa đảo Trực tuyến", css=custom_css, theme="Ocean") as demo:
        
        gr.Markdown("# 🔍 PHÂN TÍCH LỪA ĐẢO TRỰC TUYẾN")

        # ===============================================
        # KHU VỰC INPUT (Bổ sung mới)
        # ===============================================
        with gr.Row(variant="panel"):
            input_text = gr.Textbox(
                label="Nội dung cần kiểm tra:",
                placeholder="Ví dụ: Bạn đã trúng thưởng 1 tỷ. Vui lòng chuyển 100K phí xác nhận qua link rút gọn này.",
                min_width=700,
                lines=6
            )
            analyze_btn = gr.Button("🚀 Phân tích", variant="primary")
        
        gr.Markdown("---")
        
        # ===============================================
        # KHU VỰC OUTPUT (Các thành phần hiển thị kết quả)
        # ===============================================
        
        # 1. Kết quả chính (OUTPUT 1)
        with gr.Row(variant="panel") as result_row:
            # Thành phần này sẽ được cập nhật bằng HTML (qua một hàm nhỏ hoặc qua Label/Markdown)
            # Tạm thời dùng gr.Label để dễ dàng cập nhật
            result_label = gr.Markdown(
                "<h1 style='text-align: center; color: gray;'> Nhập nội dung để bắt đầu </h1>"
            )

        # 2. Mức độ Tự tin (Slider với Custom CSS Gradient) (OUTPUT 2)
        with gr.Column(variant="box", scale=2):
            gr.Markdown("## Mức độ Tự tin của Dự đoán")
            confidence_slider = gr.Slider(
                minimum=0,
                maximum=100,
                value=0, # Giá trị khởi tạo
                label="Mức độ Tự tin:",
                interactive=False,
                elem_id="confidence_slider"
            )
            
        gr.Markdown("---")
        
        # 3. Chi tiết Đặc điểm và Giải thích (OUTPUT 3 & 4)
        with gr.Row():
            # Cột 1: Các đặc điểm (OUTPUT 3)
            with gr.Column(scale=1, variant="box"): 
                gr.Markdown("## 🚩 Các Đặc điểm Được Phát hiện:")
                
                # THAY THẾ CheckboxGroup BẰNG Markdown để hiển thị chuỗi động
                features_markdown = gr.Markdown(
                    value="Kết quả đặc điểm sẽ hiển thị ở đây.",
                    label="Danh sách Đặc điểm" # Không có tác dụng trên Markdown nhưng giữ để dễ quản lý
                )
            
            # Cột 2: Giải thích (OUTPUT 4)
            with gr.Column(scale=2):
                gr.Markdown("## 📖 Giải thích Chi tiết:")
                explanation_box = gr.Textbox(
                    value="Kết quả sẽ hiển thị ở đây sau khi phân tích.",
                    label="Phân tích chuyên sâu", 
                    lines=4, 
                    interactive=False
                )

        # ===============================================
        # KẾT NỐI INPUT VÀ OUTPUT
        # ===============================================
        analyze_btn.click(
            fn=analyze_scam,
            inputs=[input_text],
            outputs=[
                result_label,        # 1. Kết quả chính (Text/Markdown)
                confidence_slider,   # 2. Mức độ tự tin (Slider)
                features_markdown,   # 3. Đặc điểm (CheckboxGroup)
                explanation_box      # 4. Giải thích (Textbox)
            ]
        )

    return demo

# Chạy giao diện
if __name__ == "__main__":
    ui = create_scam_checker_ui()
    ui.launch()