# Đây là định nghĩa class (chỉ để minh họa)
from pydantic import BaseModel, Field

class ScamDetection(BaseModel):
    CoPhaiLuaDao: str = Field(description="Có hoặc Không")
    MucDoTuTin: int = Field(description="Mức độ tự tin (0–100)")
    DacDiem: list[str] = Field(description="Danh sách đặc điểm")
    GiaiThich: str = Field(description="Giải thích ngắn gọn")

# Giả sử đây là đối tượng 'resp' bạn nhận được từ llama_index
resp = ScamDetection(
    CoPhaiLuaDao="Không",
    MucDoTuTin=95,
    DacDiem=["Giá rõ ràng", "Thông tin liên hệ đầy đủ"],
    GiaiThich="Thông tin cung cấp đầy đủ và có dấu hiệu đáng tin cậy."
)

# Chuyển đổi sang dict
response_dict = resp.model_dump()  # Hoặc resp.dict() nếu là Pydantic v1

print(response_dict)
print(type(response_dict))