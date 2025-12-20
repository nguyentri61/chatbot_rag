from app.db.mysql import get_connection

def load_documents_from_mysql():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    documents = []

    # Tournament
    cursor.execute("""
        SELECT id, name, location, start_date, end_date
        FROM tournament
    """)
    for row in cursor.fetchall():
        text = (
            f"Giải đấu {row['name']} tổ chức tại {row['location']}, "
            f"diễn ra từ {row['start_date']} đến {row['end_date']}."
        )
        documents.append(text)

    # Match
    cursor.execute("""
        SELECT round, participant1_name, participant2_name, winner_name
        FROM tournament_match
        WHERE status = 'FINISHED'
    """)
    for row in cursor.fetchall():
        text = (
            f"Trận đấu vòng {row['round']} giữa "
            f"{row['participant1_name']} và {row['participant2_name']}. "
            f"Người thắng là {row['winner_name']}."
        )
        documents.append(text)

    cursor.close()
    conn.close()
    return documents
