# RAG Chatbot với Google Gemini 🤖

Hệ thống chatbot thông minh sử dụng RAG (Retrieval-Augmented Generation) với Google Gemini để trả lời câu hỏi dựa trên dữ liệu từ MySQL và vector database.

## ✨ Tính năng

- 🔍 **RAG System**: Tìm kiếm thông tin liên quan từ vector database (FAISS)
- 🤖 **Google Gemini Integration**: Tạo câu trả lời thông minh, gọn gàng và dễ hiểu (MIỄN PHÍ)
- 💾 **MySQL Integration**: Lấy dữ liệu từ database
- 🚀 **FastAPI**: API nhanh và hiện đại
- 📝 **Markdown Formatting**: Câu trả lời được định dạng đẹp mắt

## 📋 Yêu cầu

- Python 3.8+
- MySQL Server
- Google Gemini API Key (MIỄN PHÍ)

## 🚀 Cài đặt

### 1. Clone repository

```bash
git clone <your-repo-url>
cd rag_chatbot
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Cấu hình Environment Variables

Tạo file `.env` từ `.env.example`:

```bash
cp .env.example .env
```

Chỉnh sửa file `.env` và thêm Google Gemini API key của bạn:

```env
GEMINI_API_KEY=your-gemini-api-key-here
```

**Cách lấy Google Gemini API Key (MIỄN PHÍ):**
1. Truy cập: https://aistudio.google.com/app/apikey
2. Đăng nhập với tài khoản Google của bạn
3. Nhấn "Create API Key" hoặc "Get API Key"
4. Chọn "Create API key in new project" (hoặc chọn project có sẵn)
5. Copy API key và paste vào file `.env`

**🎉 Lưu ý:** Gemini API hoàn toàn MIỄN PHÍ với quota rất cao!

### 4. Build Vector Store

```bash
python vector_store/build_index.py
```

## 🎯 Chạy ứng dụng

```bash
uvicorn app.main:app --reload --port 8000
```

Server sẽ chạy tại: http://localhost:8000

## 📚 API Documentation

Sau khi chạy server, truy cập:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoint Chat

**POST** `/api/v1/chat`

**Request Body:**
```json
{
  "message": "Câu hỏi của bạn ở đây"
}
```

**Response:**
```json
{
  "answer": "Câu trả lời được tạo bởi OpenAI GPT"
}
```

## 🎨 Ví dụ sử dụng

### Với cURL:

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Vận động viên nào tham gia giải SEA Games?"}'
```

### Với Python:

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/chat",
    json={"message": "Vận động viên nào tham gia giải SEA Games?"}
)

print(response.json()["answer"])
```

## ⚙️ Cấu hình

### Thay đổi model Gemini

Trong file `app/rag/generator.py`, bạn có thể thay đổi model:

```python
model = genai.GenerativeModel('gemini-1.5-flash')  # Model mặc định (nhanh, MIỄN PHÍ)
# model = genai.GenerativeModel('gemini-1.5-pro')  # Model tốt hơn (chật lượng cao hơn)
# model = genai.GenerativeModel('gemini-pro')      # Phiên bản cũ
```

### Điều chỉnh tham số Gemini

```python
temperature=0.7,          # Độ sáng tạo (0-1)
max_output_tokens=500,    # Độ dài câu trả lời
top_p=0.95,              # Điều khiển đa dạng từ
```

## 📁 Cấu trúc thư mục

```
rag_chatbot/
├── app/
│   ├── main.py              # FastAPI app chính
│   ├── api/
│   │   └── chat.py          # Chat endpoint
│   ├── db/
│   │   └── mysql.py         # MySQL connection
│   ├── models/
│   │   └── schemas.py       # Pydantic models
│   └── rag/
│       ├── generator.py     # OpenAI GPT generator
│       ├── retriever.py     # Vector search
│       └── mysql_loader.py  # Load data từ MySQL
├── vector_store/
│   ├── build_index.py       # Build FAISS index
│   ├── vector_store.py      # Vector store operations
│   └── faiss.index          # FAISS vector database
├── .env.example             # Template cho environment variables
├── .gitignore              # Git ignore file
├── requirements.txt         # Python dependencies
└── README.md               # Tài liệu này
```

## 💡 Tips sử dụng

1. **MIỄN PHÍ 100%**: Gemini API hoàn toàn miễn phí với quota cao.
2. **Chất lượng**: Gemini 1.5 Flash tương đương GPT-3.5, Gemini 1.5 Pro tương đương GPT-4.
3. **Tốc độ**: Gemini Flash rất nhanh, phù hợp cho production.
4. **Prompt Engineering**: Chỉnh sửa prompt trong `generator.py` để tùy chỉnh cách Gemini trả lời.
5. **Error Handling**: Hệ thống có fallback nếu Gemini API lỗi.

## 🐛 Troubleshooting

### Lỗi "Gemini API Error"
- Kiểm tra API key trong file `.env`
- Kiểm tra internet connection
- Thử tạo API key mới tại: https://aistudio.google.com/app/apikey

### Lỗi "No module named 'google.generativeai'"
```bash
pip install google-generativeai python-dotenv
```

### Lỗi quota (không khả năng xảy ra với Gemini)
Gemini có quota miễn phí rất cao, hiếm khi gặp lỗi này.

## 📝 License

MIT License

## 👨‍💻 Tác giả

TLCN Project