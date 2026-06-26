from sqlalchemy.orm import Session
from app.database.models import ChatHistory


def save_chat(
    db: Session,
    user_id: int,
    question: str,
    response: str
):
    chat = ChatHistory(
        user_id=user_id,
        question=question,
        response=response
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat


def get_chat_history(
    db: Session,
    user_id: int
):
    return (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.created_at.desc())
        .all()
    )