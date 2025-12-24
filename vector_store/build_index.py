import faiss
import pickle
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from app.db.mysql import get_connection

INDEX_PATH = "vector_store/faiss.index"
META_PATH = "vector_store/meta.pkl"

# Use free local embedding model
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def embed(text: str):
    return model.encode(text, convert_to_numpy=True).astype('float32')

def build_index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    vectors, metadata = [], []

    # 1. Lịch sử tham gia giải đấu của vận động viên
    print("📊 Đang đọc player_tournament_history...")
    cursor.execute("""
        SELECT 
            t.name AS tournament,
            c.category AS category,
            pth.final_ranking,
            pth.prize,
            pth.old_level,
            pth.new_level,
            ui.full_name,
            ui.gender,
            a.reputation_score,
            pth.created_at
        FROM player_tournament_history pth
        JOIN accounts a ON a.id = pth.player_id
        LEFT JOIN user_info ui ON ui.account_id = a.id
        JOIN tournament_categories c ON c.id = pth.category_id
        JOIN tournaments t ON t.id = c.tournament_id
    """)
    
    for r in cursor.fetchall():
        text = (
            f"Vận động viên {r['full_name']} ({r['gender']}) "
            f"tham gia giải {r['tournament']} "
            f"hạng mục {r['category']} "
            f"xếp hạng {r['final_ranking'] or 'chưa xác định'} "
            f"nhận giải {r['prize'] or 'không có'}. "
            f"Điểm uy tín: {r['reputation_score']}. "
            f"Trình độ từ {r['old_level'] or 'N/A'} lên {r['new_level'] or 'N/A'}."
        )
        vectors.append(embed(text))
        metadata.append(text)

    # 2. Thông tin giải đấu
    print("🏆 Đang đọc tournaments...")
    cursor.execute("""
        SELECT 
            name,
            description,
            location,
            start_date,
            end_date,
            registration_start_date,
            registration_end_date,
            status,
            rules
        FROM tournaments
    """)
    
    for r in cursor.fetchall():
        text = (
            f"Giải đấu {r['name']} "
            f"tổ chức tại {r['location']} "
            f"từ {r['start_date']} đến {r['end_date']}. "
            f"Trạng thái: {r['status']}. "
            f"Đăng ký từ {r['registration_start_date']} đến {r['registration_end_date']}. "
            f"Mô tả: {r['description'] or 'Không có'}."
        )
        vectors.append(embed(text))
        metadata.append(text)

    # 3. Hạng mục giải đấu
    print("📋 Đang đọc tournament_categories...")
    cursor.execute("""
        SELECT 
            t.name AS tournament,
            c.category,
            c.min_level,
            c.max_level,
            c.max_participants,
            c.registration_fee,
            c.first_prize,
            c.second_prize,
            c.third_prize,
            c.registration_deadline
        FROM tournament_categories c
        JOIN tournaments t ON t.id = c.tournament_id
    """)
    
    for r in cursor.fetchall():
        text = (
            f"Giải {r['tournament']} "
            f"hạng mục {r['category']} "
            f"dành cho trình độ từ {r['min_level'] or 0} đến {r['max_level'] or 5}. "
            f"Số người tối đa: {r['max_participants']}. "
            f"Phí: {r['registration_fee'] or 0} VNĐ. "
            f"Giải thưởng: Nhất {r['first_prize'] or 'N/A'}, Nhì {r['second_prize'] or 'N/A'}, Ba {r['third_prize'] or 'N/A'}. "
            f"Hạn đăng ký: {r['registration_deadline']}. "
        )
        vectors.append(embed(text))
        metadata.append(text)

    # 4. Thông tin vận động viên
    print("👤 Đang đọc user_info & accounts...")
    cursor.execute("""
        SELECT 
            ui.full_name,
            ui.gender,
            ui.birth_date,
            ui.address,
            ui.bio,
            ui.phone,
            a.email,
            a.reputation_score,
            a.total_participated_events,
            pr.skill_level,
            pr.overall_score,
            pr.experience,
            pr.stamina
        FROM user_info ui
        JOIN accounts a ON a.id = ui.account_id
        LEFT JOIN player_rating pr ON pr.account_id = a.id
        WHERE EXISTS (
            SELECT 1 FROM account_roles ar 
            JOIN roles r ON r.id = ar.role_id 
            WHERE ar.account_id = a.id AND r.name = 'PLAYER'
        )
    """)
    
    for r in cursor.fetchall():
        text = (
            f"Vận động viên {r['full_name']} "
            f"giới tính {r['gender']}, sinh năm {r['birth_date'] or 'N/A'}, "
            f"địa chỉ {r['address'] or 'chưa cập nhật'}. "
            f"Trình độ: {r['skill_level'] or 'chưa đánh giá'} "
            f"({r['overall_score'] or 0} điểm). "
            f"Kinh nghiệm: {r['experience'] or 0}/10, Thể lực: {r['stamina'] or 0}/10. "
            f"Điểm uy tín: {r['reputation_score']}, "
            f"đã tham gia {r['total_participated_events']} sự kiện. "
            f"Tiểu sử: {r['bio'] or 'Chưa có'}."
        )
        vectors.append(embed(text))
        metadata.append(text)

    # 5. Câu lạc bộ
    print("🏢 Đang đọc clubs...")
    cursor.execute("""
        SELECT 
            c.name,
            c.description,
            c.location,
            c.visibility,
            c.status,
            c.max_members,
            c.min_level,
            c.max_level,
            c.reputation,
            ui.full_name AS owner_name,
            f.name AS facility_name,
            f.address AS facility_address
        FROM clubs c
        LEFT JOIN accounts a ON a.id = c.owner_id
        LEFT JOIN user_info ui ON ui.account_id = a.id
        LEFT JOIN facilities f ON f.id = c.facility_id
    """)
    
    for r in cursor.fetchall():
        text = (
            f"Câu lạc bộ {r['name']} "
            f"do {r['owner_name']} quản lý. "
            f"Địa điểm: {r['location'] or 'chưa rõ'}. "
            f"Sân tập: {r['facility_name'] or 'chưa có'} tại {r['facility_address'] or ''}. "
            f"Trạng thái: {r['status']}, Độ hiển thị: {r['visibility']}. "
            f"Số thành viên tối đa: {r['max_members']}, "
            f"trình độ từ {r['min_level']} đến {r['max_level']}. "
            f"Điểm uy tín: {r['reputation'] or 'N/A'}. "
            f"Mô tả: {r['description'] or 'Không có'}."
        )
        vectors.append(embed(text))
        metadata.append(text)

    # 6. Sự kiện câu lạc bộ
    print("🎉 Đang đọc club_events...")
    cursor.execute("""
        SELECT 
            ce.title,
            ce.description,
            ce.location,
            ce.start_time,
            ce.end_time,
            ce.fee,
            ce.deadline,
            ce.status,
            ce.max_club_members,
            ce.max_outside_members,
            ce.min_level,
            ce.max_level,
            c.name AS club_name,
            f.name AS facility_name
        FROM club_events ce
        LEFT JOIN clubs c ON c.id = ce.club_id
        LEFT JOIN facilities f ON f.id = ce.facility_id
        LIMIT 500
    """)
    
    for r in cursor.fetchall():
        text = (
            f"Sự kiện '{r['title']}' "
            f"của CLB {r['club_name'] or 'Độc lập'} "
            f"diễn ra từ {r['start_time']} đến {r['end_time']} "
            f"tại {r['location'] or r['facility_name'] or 'chưa rõ'}. "
            f"Phí tham gia: {r['fee'] or 0} VNĐ. "
            f"Hạn đăng ký: {r['deadline']}. "
            f"Số chỗ: {r['max_club_members']} (thành viên CLB), "
            f"{r['max_outside_members']} (bên ngoài). "
            f"Trình độ: {r['min_level']}-{r['max_level']}. "
            f"Trạng thái: {r['status']}."
        )
        vectors.append(embed(text))
        metadata.append(text)

    # 7. Trận đấu giải đấu
    print("⚔️ Đang đọc tournament_match...")
    cursor.execute("""
        SELECT 
            tm.round,
            tm.match_index,
            tm.participant1name,
            tm.participant2name,
            tm.winner_name,
            tm.status,
            tm.start_time,
            t.name AS tournament,
            c.category
        FROM tournament_match tm
        JOIN tournament_categories c ON c.id = tm.category_id
        JOIN tournaments t ON t.id = c.tournament_id
        WHERE tm.status = 'COMPLETED'
        LIMIT 1000
    """)
    
    for r in cursor.fetchall():
        text = (
            f"Trận đấu vòng {r['round']} trận {r['match_index']} "
            f"tại giải {r['tournament']} hạng mục {r['category']}: "
            f"{r['participant1_name']} vs {r['participant2_name']}. "
            f"Người thắng: {r['winner_name'] or 'chưa rõ'}. "
            f"Ngày thi đấu: {r['start_time']}."
        )
        vectors.append(embed(text))
        metadata.append(text)

    # 8. Đội đôi tham gia giải
    print("👥 Đang đọc tournament_teams...")
    cursor.execute("""
        SELECT 
            tt.team_name,
            tt.status,
            u1.full_name AS player1,
            u2.full_name AS player2,
            t.name AS tournament,
            c.category
        FROM tournament_teams tt
        JOIN accounts a1 ON a1.id = tt.player1_id
        JOIN accounts a2 ON a2.id = tt.player2_id
        JOIN user_info u1 ON u1.account_id = a1.id
        JOIN user_info u2 ON u2.account_id = a2.id
        JOIN tournament_categories c ON c.id = tt.category_id
        JOIN tournaments t ON t.id = c.tournament_id
    """)
    
    for r in cursor.fetchall():
        text = (
            f"Đội {r['team_name']} "
            f"gồm {r['player1']} và {r['player2']} "
            f"tham gia giải {r['tournament']} hạng mục {r['category']}. "
            f"Trạng thái: {r['status']}."
        )
        vectors.append(embed(text))
        metadata.append(text)

    # 9. Kết quả giải đấu
    print("🏅 Đang đọc tournament_results...")
    cursor.execute("""
        SELECT 
            tr.ranking,
            tr.prize,
            ui.full_name AS player_name,
            tt.team_name,
            t.name AS tournament,
            c.category
        FROM tournament_results tr
        LEFT JOIN tournament_participants tp ON tp.id = tr.participant_id
        LEFT JOIN accounts a ON a.id = tp.account_id
        LEFT JOIN user_info ui ON ui.account_id = a.id
        LEFT JOIN tournament_teams tt ON tt.id = tr.team_id
        JOIN tournament_categories c ON c.id = tr.category_id
        JOIN tournaments t ON t.id = c.tournament_id
    """)
    
    for r in cursor.fetchall():
        player_info = r['player_name'] or r['team_name'] or 'Không rõ'
        text = (
            f"Xếp hạng {r['ranking']} tại giải {r['tournament']} "
            f"hạng mục {r['category']}: {player_info}. "
            f"Giải thưởng: {r['prize'] or 'không có'}."
        )
        vectors.append(embed(text))
        metadata.append(text)

    # 10. Đánh giá sự kiện
    print("⭐ Đang đọc club_event_ratings...")
    cursor.execute("""
        SELECT 
            cer.rating,
            cer.comment,
            cer.club_member,
            ui.full_name,
            ce.title AS event_title,
            c.name AS club_name
        FROM club_event_ratings cer
        JOIN accounts a ON a.id = cer.account_id
        JOIN user_info ui ON ui.account_id = a.id
        JOIN club_events ce ON ce.id = cer.club_event_id
        LEFT JOIN clubs c ON c.id = ce.club_id
        WHERE cer.comment IS NOT NULL AND cer.comment != ''
        LIMIT 500
    """)
    
    for r in cursor.fetchall():
        text = (
            f"{r['full_name']} "
            f"({'thành viên CLB' if r['club_member'] else 'khách'}) "
            f"đánh giá {r['rating']}/5 sao cho sự kiện '{r['event_title']}' "
            f"của {r['club_name'] or 'tổ chức độc lập'}. "
            f"Nhận xét: {r['comment'][:200]}."
        )
        vectors.append(embed(text))
        metadata.append(text)

    # 11. Cơ sở vật chất
    print("🏟️ Đang đọc facilities...")
    cursor.execute("""
        SELECT 
            name,
            address,
            district,
            city,
            location
        FROM facilities
    """)
    
    for r in cursor.fetchall():
        text = (
            f"Sân cầu lông {r['name']} "
            f"tại {r['address']}, {r['district']}, {r['city']}. "
            f"Vị trí: {r['location']}."
        )
        vectors.append(embed(text))
        metadata.append(text)

    # Build FAISS index
    # 11. Hướng dẫn sử dụng UI (FAQ)
    print("❓ Đang đọc ui_instructions...")
    cursor.execute("""
        SELECT 
            question,
            instruction,
            category,
            keywords
        FROM ui_instructions
    """)
    
    for r in cursor.fetchall():
        # Thêm câu hỏi vào vector store
        text = f"Câu hỏi: {r['question']}\n\nHướng dẫn: {r['instruction']}\n\nDanh mục: {r['category']}"
        vectors.append(embed(text))
        metadata.append(text)
        
        # Thêm keywords để tìm kiếm tốt hơn
        if r['keywords']:
            keywords_text = f"Hướng dẫn về: {r['keywords']}. {r['instruction']}"
            vectors.append(embed(keywords_text))
            metadata.append(text)  # Vẫn trả về full instruction

    if not vectors:
        print("❌ Không có dữ liệu trong database!")
        return
    
    print(f"\n🔨 Đang xây dựng FAISS index với {len(vectors)} bản ghi...")
    dim = len(vectors[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(vectors))

    os.makedirs("vector_store", exist_ok=True)
    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "wb") as f:
        pickle.dump(metadata, f)

    cursor.close()
    conn.close()
    
    print(f"\n✅ Hoàn tất! Đã xây dựng vector store với {len(metadata)} bản ghi")
    print("   📊 Lịch sử giải đấu")
    print("   🏆 Thông tin giải đấu & hạng mục")
    print("   👤 Hồ sơ vận động viên")
    print("   🏢 Câu lạc bộ")
    print("   🎉 Sự kiện CLB")
    print("   ⚔️ Trận đấu")
    print("   👥 Đội đôi")
    print("   🏅 Kết quả giải đấu")
    print("   ⭐ Đánh giá sự kiện")
    print("   🏟️ Cơ sở vật chất")
    print("   ❓ Hướng dẫn sử dụng UI")

if __name__ == "__main__":
    build_index()