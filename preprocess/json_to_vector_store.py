# ============================================================
# Convert structured JSON (content.json) → Vector Database (Chroma)
# with multilingual embedding model: BAAI/bge-m3
# ============================================================

# 🔧 Cài đặt thư viện (chạy 1 lần trong terminal)
# pip install llama-index
# pip install llama-index-embeddings-huggingface
# pip install llama-index-vector-stores-chroma
# pip install chromadb
# pip install sentence-transformers

import json
from pathlib import Path
from llama_index.core import (
    Document,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)
from llama_index.llms.gemini import Gemini
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from chromadb import Client


# ============================================================
# 1️⃣ Đọc dữ liệu JSON
# ============================================================

DATA_PATH = Path("content.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# ============================================================
# 2️⃣ Chuyển JSON lồng nhau → danh sách Document
# ============================================================

def flatten_json_to_documents(data):
    documents = []

    def process_section(section_name, section_content):
        if isinstance(section_content, list):
            for item in section_content:
                text_parts = []
                for key, value in item.items():
                    if isinstance(value, list):
                        joined = "; ".join(value)
                        text_parts.append(f"{key}: {joined}")
                    else:
                        text_parts.append(f"{key}: {value}")
                text = f"Phần: {section_name}\n" + "\n".join(text_parts)
                documents.append(Document(text=text, metadata={"section": section_name}))

        elif isinstance(section_content, dict):
            text_parts = []
            for k, v in section_content.items():
                if isinstance(v, list):
                    joined = "; ".join(v)
                    text_parts.append(f"{k}: {joined}")
            text = f"Phần: {section_name}\n" + "\n".join(text_parts)
            documents.append(Document(text=text, metadata={"section": section_name}))

    for key, value in data.items():
        process_section(key, value)

    return documents


documents = flatten_json_to_documents(data)
print(f"✅ Tạo {len(documents)} documents từ file JSON.")

# ============================================================
# 3️⃣ Tạo Embedding Model (BAAI/bge-m3)
# ============================================================

embed_model = HuggingFaceEmbedding(model_name="intfloat/multilingual-e5-base", 
    cache_folder="./models")
Settings.embed_model = embed_model

# Tạo service context cho index
# service_context = ServiceContext.from_defaults()

# ============================================================
# 4️⃣ Tạo Vector Store (Chroma)
# ============================================================

client = Client()
collection = client.create_collection("scam_detection_bge")
vector_store = ChromaVectorStore(chroma_collection=collection)

# ============================================================
# 5️⃣ Tạo Index từ Documents
# ============================================================

index = VectorStoreIndex.from_documents(
    documents,
    vector_store=vector_store,
)

index.storage_context.persist("./storage_bge")

print("✅ Index đã được tạo với BAAI/bge-m3 và lưu thành công!")

# Dùng Gemini 1.5 Flash

# ============================================================
# 6️⃣ Truy vấn thử nghiệm
# ============================================================

# query_engine = index.as_query_engine()

# queries = [
#     "Những dấu hiệu nhận biết tài khoản giả mạo là gì?",
#     "Ví dụ về tin nhắn lừa đảo tuyển dụng?",
#     "Các đặc điểm của bài đăng đầu tư ảo?",
# ]

# for q in queries:
#     print(f"\n🧠 Câu hỏi: {q}")
#     response = query_engine.query(q)
#     print("💬 Trả lời:", response)

# ============================================================
# 7️⃣ (Tuỳ chọn) Tải lại index đã lưu
# ============================================================
# storage_context = StorageContext.from_defaults(persist_dir="./storage_bge")
# index = load_index_from_storage(storage_context, service_context=service_context)
# query_engine = index.as_query_engine()
# print(query_engine.query("Dấu hiệu nghi ngờ khi xem avatar là gì?"))
