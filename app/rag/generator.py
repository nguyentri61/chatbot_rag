import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Load environment variables
load_dotenv()

# Initialize Google Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_answer(query: str, context: list[str]) -> str:
    """Generate answer using Google Gemini based on retrieved context"""
    
    # Prepare context for Gemini
    if context and len(context) > 0:
        context_text = "\n\n".join(context[:5])
        has_context = True
    else:
        context_text = "Không có thông tin cụ thể trong cơ sở dữ liệu."
        has_context = False
    
    # Create prompt for Gemini with flexible answering capability
    if has_context:
        prompt = f"""Bạn là một trợ lý AI thông minh và hữu ích của trang web cộng đồng cầu lông BadmintonNet. 
Nhiệm vụ của bạn là trả lời câu hỏi dựa trên thông tin được cung cấp.

Quy tắc trả lời:
1. Trả lời bằng tiếng Việt, gọn gàng và dễ hiểu
2. Sử dụng định dạng markdown để làm đẹp câu trả lời (**, *, •, số thứ tự)
3. Ưu tiên sử dụng thông tin từ ngữ cảnh được cung cấp
4. Nếu thông tin không đủ hoặc câu hỏi mang tính tổng quát, hãy bổ sung kiến thức chung hợp lý
5. Trình bày có cấu trúc, logic và mạch lạc
6. Tóm tắt ngắn gọn, dễ hiểu
7. Cầu trả lời đúng ngôn ngữ tự nhiên và không lang mang trả lời các vấn đề ngoài lề
8. Gợi ý thêm câu hỏi khác cho người dùng.

Thông tin từ cơ sở dữ liệu:

{context_text}

Câu hỏi: {query}

Hãy trả lời câu hỏi một cách đầy đủ và hữu ích nhất."""
    else:
        # For questions without context, allow Gemini to use general knowledge
        prompt = f"""Bạn là một trợ lý AI thông minh trang web cộng đồng cầu lông BadmintonNet.
Người dùng hỏi về: {query}

Mặc dù không có thông tin cụ thể trong cơ sở dữ liệu, hãy:
1. Trả lời bằng tiếng Việt, gọn gàng và dễ hiểu
2. Sử dụng kiến thức chung về thể thao để đưa ra câu trả lời hữu ích
3. Sử dụng định dạng markdown (**, *, •, số thứ tự)
4. Trình bày có cấu trúc, từng bước rõ ràng
5. Nếu là câu hỏi về "cách tham gia", "quy trình", "thủ tục" - hãy đưa ra hướng dẫn tổng quát
6. Giữ câu trả lời ngắn gọn (3-5 bước chính)
7. Cầu trả lời đúng ngôn ngữ tự nhiên và không lang mang trả lời các vấn đề ngoài lề
8. Gợi ý thêm câu hỏi khác cho người dùng.

Lưu ý: Đây là câu trả lời tổng quát vì chưa có thông tin cụ thể trong hệ thống."""

    try:
        # Generate content with new API
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=500,
                top_p=0.95,
            )
        )
        
        answer = response.text.strip()
        return answer
        
    except Exception as e:
        # Fallback to simple response if API fails
        print(f"Gemini API Error: {e}")
        if has_context:
            return f"**Thông tin tìm thấy:**\n\n{context_text}"
        else:
            return "Xin lỗi, hiện tại hệ thống không thể trả lời câu hỏi này. Vui lòng thử lại sau."