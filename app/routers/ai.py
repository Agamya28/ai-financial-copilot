from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.ai import ChatRequest, ChatResponse
from app.services.financial_analyst import analyze_question
from app.services.financial_report import generate_financial_report
from app.services.chat_history import save_chat, get_chat_history

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    response = analyze_question(
        question=request.question,
        db=db,
        user_id=current_user.id
    )

    save_chat(
    db=db,
    user_id=current_user.id,
    question=request.question,
    response=response
    )

    return ChatResponse(
        response=response
    )

@router.get("/report")
def get_ai_report(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    report = generate_financial_report(
        db=db,
        user_id=current_user.id
    )

    return {
        "report": report
    }

@router.get("/history")
def chat_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_chat_history(
        db=db,
        user_id=current_user.id
    )