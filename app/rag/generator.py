import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

def generate_answer(query: str, context: list[str]) -> str:
    """Generate answer based on context"""
    
    if not context:
        return "Xin lỗi, hệ thống chưa có thông tin về câu hỏi này."
    
    # Extract tournament info
    tournament_info = {}
    for ctx in context:
        if "tham gia giải" in ctx:
            parts = ctx.split("tham gia giải")
            if len(parts) >= 2:
                player = parts[0].replace("Vận động viên", "").strip()
                details = parts[1].strip()
                
                if player not in tournament_info:
                    tournament_info[player] = details
    
    if not tournament_info:
        return "\n".join(context[:5])
    
    # Format response
    response = f"**Thông tin về giải đấu:**\n\n"
    
    for player, details in list(tournament_info.items())[:5]:
        response += f"• Vận động viên **{player}** {details}\n"
    
    return response