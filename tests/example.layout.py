import gradio as gr

# Dữ liệu mẫu sẽ được trả về sau khi "phân tích"
def get_mock_analysis(input_text):
    """Mô phỏng hàm phân tích lừa đảo, trả về dữ liệu mẫu."""
    # Logic đơn giản: nếu input chứa 'chuyển tiền' -> Tự tin cao
    if "chuyển tiền" in input_text.lower() or "nhận thưởng" in input_text.lower():
        return {
            "CoPhaiLuaDao": "Có",
            "MucDoTuTin": 95,
            "DacDiem": ["Yêu cầu chuyển tiền", "Mạo danh người nổi tiếng", "Dùng link rút gọn bất thường"],
            "GiaiThich": f"Nội dung được phân tích có dấu hiệu rõ ràng của hành vi lừa đảo trực tuyến, đặc biệt nhấn mạnh vào yêu cầu tài chính. (Đầu vào: '{input_text[:50]}...')"
        }
    else:
        return {
            "CoPhaiLuaDao": "Không",
            "MucDoTuTin": 15,
            "DacDiem": ["Không phát hiện dấu hiệu bất thường"],
            "GiaiThich": f"Nội dung này có vẻ an toàn, mức độ rủi ro thấp. Vẫn cần thận trọng. (Đầu vào: '{input_text[:50]}...')"
        }


# CSS cho Gradient (Giữ nguyên)
custom_css = """
#confidence_slider .wrap-inner .slider-fill {
    background-image: linear-gradient(to right, #4CAF50, #FFEB3B, #F44336) !important;
    background-color: transparent !important; 
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