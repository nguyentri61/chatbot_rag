# Hướng dẫn thêm UI Instructions vào Chatbot

## 📚 Tổng quan

Để chatbot có thể trả lời các câu hỏi về thao tác UI như "Làm thế nào để tạo CLB?", bạn cần:
1. Tạo bảng `ui_instructions` trong MySQL
2. Thêm dữ liệu hướng dẫn
3. Rebuild vector store
4. Test chatbot

---

## 🚀 Các bước thực hiện

### **Bước 1: Import dữ liệu vào MySQL**

```bash
# Kết nối MySQL
mysql -u root -p sports_net

# Hoặc dùng MySQL Workbench/phpMyAdmin
```

Chạy file SQL:
```bash
source D:\TLCN\rag_chatbot\docs\ui_instructions.sql
```

Hoặc copy-paste nội dung file [ui_instructions.sql](ui_instructions.sql) vào MySQL client.

---

### **Bước 2: Kiểm tra dữ liệu**

```sql
-- Xem tất cả hướng dẫn
SELECT * FROM ui_instructions;

-- Đếm số lượng
SELECT COUNT(*) FROM ui_instructions;

-- Xem theo category
SELECT category, COUNT(*) as count 
FROM ui_instructions 
GROUP BY category;
```

---

### **Bước 3: Rebuild vector store**

```bash
cd D:\TLCN\rag_chatbot
python vector_store\build_index.py
```

Kết quả sẽ hiển thị:
```
✅ Hoàn tất! Đã xây dựng vector store với XXX bản ghi
   ...
   ❓ Hướng dẫn sử dụng UI
```

---

### **Bước 4: Test chatbot**

Khởi động lại server:
```bash
uvicorn app.main:app --reload --port 8000
```

Test các câu hỏi:
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Làm thế nào để tạo một CLB?"}'
```

Hoặc dùng Swagger UI: http://localhost:8000/docs

---

## ✍️ Thêm hướng dẫn mới

### Cách 1: Thêm trực tiếp vào MySQL

```sql
INSERT INTO ui_instructions (question, instruction, category, keywords) 
VALUES (
    'Làm sao để xóa tài khoản?',
    '**Cách xóa tài khoản:**
    
1. Vào **Cài đặt** → **Tài khoản**
2. Kéo xuống cuối trang
3. Nhấn **"Xóa tài khoản"**
4. Xác nhận quyết định
5. Nhập mật khẩu để xác thực

**Cảnh báo:** Hành động này không thể hoàn tác!',
    'Account',
    'xóa tài khoản, delete account, hủy tài khoản'
);
```

### Cách 2: Import từ file Excel/CSV

1. Chuẩn bị file `instructions.csv`:
```csv
question,instruction,category,keywords
"Làm sao upload ảnh?","Các bước...",Upload,"upload, đăng ảnh"
```

2. Import vào MySQL:
```sql
LOAD DATA LOCAL INFILE 'instructions.csv'
INTO TABLE ui_instructions
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(question, instruction, category, keywords);
```

### Sau khi thêm, nhớ rebuild:
```bash
python vector_store\build_index.py
```

---

## 📋 Template mẫu cho instruction

```sql
INSERT INTO ui_instructions (question, instruction, category, keywords) VALUES
('Câu hỏi của người dùng?',
'**Tiêu đề hướng dẫn:**

1. **Bước 1**: Mô tả chi tiết
   • Chi tiết phụ 1
   • Chi tiết phụ 2
2. **Bước 2**: Tiếp tục
3. **Bước 3**: Kết thúc

**Lưu ý:** Thông tin quan trọng cần nhớ.',
'Category Name',
'keyword1, keyword2, từ khóa liên quan');
```

---

## 🎯 Best Practices

### 1. **Viết câu hỏi đa dạng**
```sql
-- Tốt: Bao gồm nhiều cách hỏi
keywords: 'tạo CLB, tạo club, thêm CLB, CLB mới, tạo câu lạc bộ'

-- Tránh: Chỉ 1 từ khóa
keywords: 'tạo CLB'
```

### 2. **Sử dụng Markdown**
- `**Bold**` cho tiêu đề và từ khóa quan trọng
- `•` hoặc số thứ tự cho các bước
- Ngắt dòng rõ ràng

### 3. **Phân loại Category**
```
- Account: Tài khoản
- CLB Management: Quản lý CLB
- Tournament: Giải đấu
- Activity: Hoạt động
- Schedule: Lịch thi đấu
- Notification: Thông báo
- Upload: Tải lên
- Settings: Cài đặt
```

### 4. **Keywords hiệu quả**
- Bao gồm cả tiếng Việt và tiếng Anh
- Thêm các từ đồng nghĩa
- Bao gồm cả lỗi chính tả phổ biến

---

## 🔍 Tìm kiếm và Debug

### Kiểm tra vector search
```python
from vector_store.vector_store import search

# Test search
results = search("Làm thế nào để tạo CLB?", top_k=3)
for r in results:
    print(r['text'])
    print('---')
```

### Xem log
```bash
# Xem log của generator
tail -f app/rag/generator.py
```

---

## 💡 Tips

1. **Thêm dần dần**: Bắt đầu với 10-20 câu hỏi quan trọng nhất
2. **Thu thập từ người dùng**: Xem log để biết họ hỏi gì
3. **Cập nhật thường xuyên**: Khi UI thay đổi, cập nhật hướng dẫn
4. **Versioning**: Thêm cột `version` để quản lý phiên bản

---

## ❓ Troubleshooting

### Chatbot không trả lời đúng?
1. Kiểm tra dữ liệu đã import chưa: `SELECT COUNT(*) FROM ui_instructions;`
2. Đã rebuild vector store chưa?
3. Keywords có phù hợp không?
4. Thử tăng `top_k` trong search

### Câu trả lời không đẹp?
1. Kiểm tra format Markdown trong instruction
2. Đảm bảo có xuống dòng rõ ràng
3. Sử dụng **bold** và • bullets

### Tốc độ chậm?
1. Giảm `max_output_tokens` trong generator.py
2. Tối ưu keywords (bớt từ khóa không cần thiết)
3. Cache kết quả cho câu hỏi phổ biến

---

## 📞 Cần giúp đỡ?

Nếu gặp vấn đề, kiểm tra:
1. MySQL connection trong `app/db/mysql.py`
2. Vector store có tồn tại: `vector_store/faiss.index`
3. Gemini API key hợp lệ
4. Log lỗi trong terminal

---

Chúc bạn thành công! 🎉
