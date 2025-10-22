from llama_index.core import (
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from llama_index.llms.gemini import Gemini
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.prompts import PromptTemplate

class ScamDetection(BaseModel):
    CoPhaiLuaDao: str = Field(description="Có hoặc Không")
    MucDoTuTin: int = Field(description="Mức độ tự tin (0–100)")
    DacDiem: list[str] = Field(description="Danh sách đặc điểm")
    GiaiThich: str = Field(description="Giải thích ngắn gọn")

embed_model = HuggingFaceEmbedding(model_name="intfloat/multilingual-e5-base", 
    cache_folder="./models")
llm = Gemini(api_key="....") # Điền API KEY ở đây ::>
Settings.llm = llm
Settings.embed_model = embed_model


scam_prompt = PromptTemplate(
"""
Bạn là chuyên gia an toàn thông tin có nhiệm vụ phát hiện và phân loại các hành vi lừa đảo trực tuyến trên mạng xã hội Việt Nam.

Hãy đọc kỹ ngữ cảnh dưới đây, sau đó điền các trường tương ứng trong JSON:
{
  "CoPhaiLuaDao": "Có | Không | Không xác định",
  "MucDoTuTin": 0–100,
  "DacDiem": ["chuỗi", "chuỗi", ...],
  "GiaiThich": "chuỗi"
}

⚠️ Yêu cầu:
- Chỉ trả về JSON hợp lệ, không thêm chữ hay ký hiệu khác.
- Nếu không có thông tin phù hợp, để "Không xác định" hoặc giá trị trống.

Ngữ cảnh:
{context_str}

Câu hỏi người dùng:
{query_str}
"""
)

parser = PydanticOutputParser(ScamDetection)
storage_context = StorageContext.from_defaults(persist_dir="./patterns")
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine(
    text_qa_template=scam_prompt, 
    output_parser=parser)

# print(query_engine.query("Tin cực shock, cực shock. Tin được không? Truy cập link https://... để nhận ngay ưu đãi hấp dẫn và cơ hội trúng 10 tỷ"))