from database import get_connection


def save_feedback(candidate_id, feedback_type, comment):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO feedback (candidate_id, feedback_type, comment) VALUES (?, ?, ?)",
        (candidate_id, feedback_type, comment)
    )

    conn.commit()
    conn.close()

    return {
        "message": "Feedback saved successfully",
        "candidate_id": candidate_id,
        "feedback_type": feedback_type
    }