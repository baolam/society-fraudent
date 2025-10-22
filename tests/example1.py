import gradio as gr
import json
# from chatbot_configure import query_engine

# Giống hàm normalize_response trong bản Tkinter
def normalize_response(resp):
    if hasattr(resp, "dict"):  # pydantic object
        return resp.dict()
    if isinstance(resp, dict):
        return resp
    try:
        return json.loads(resp)
    except Exception:
        return {"GiaiThich": str(resp)}

def run_query(query):
    # ⚙️ Nếu có query_engine thật:
    # resp = query_engine.query(query, extra_info={"category": category})
    # return resp
    #
    # Dưới đây là mock data:
    return {
        "CoPhaiLuaDao": "Có",
        "MucDoTuTin": 92,
        "DacDiem": [
            "Mạo danh người nổi tiếng",
            "Yêu cầu chuyển tiền",
            "Dùng link rút gọn bất thường"
        ],
        "GiaiThich": "Nội dung có đặc điểm rõ ràng của hành vi lừa đảo trực tuyến."
    }

# Giao diện callback
def analyze(query, category=None):
    if not query.strip():
        return "❌ Vui lòng nhập câu hỏi", None

    resp = run_query(query)
    norm = normalize_response(resp)
    pretty = json.dumps(norm, ensure_ascii=False, indent=2)
    return (
        f"**Có phải lừa đảo:** {norm.get('CoPhaiLuaDao', 'Không xác định')}\n\n"
        f"**Mức độ tự tin:** {norm.get('MucDoTuTin', 0)}%\n\n"
        f"**Đặc điểm:**\n" + "\n".join(f"- {d}" for d in norm.get("DacDiem", [])) + "\n\n"
        f"**Giải thích:**\n{norm.get('GiaiThich', '')}",
        pretty
    )

with gr.Blocks(theme=gr.themes.Soft(primary_hue="red")) as demo:
    gr.Markdown("## 🧠 Hệ thống phát hiện hành vi lừa đảo trực tuyến (phiên bản gọn)")
    
    query = gr.Textbox(
        label="Câu hỏi người dùng",
        placeholder="Ví dụ: Tin nhắn yêu cầu nạp thẻ để nhận thưởng có phải lừa đảo không?",
        lines=2
    )
    
    analyze_btn = gr.Button("🔍 Phân tích")
    
    result_md = gr.Markdown(label="Kết quả phân tích")
    raw_json = gr.JSON(label="Kết quả JSON (raw)")
    
    analyze_btn.click(analyze, inputs=query, outputs=[result_md, raw_json])

demo.launch(server_name="0.0.0.0", server_port=7860, share=True)