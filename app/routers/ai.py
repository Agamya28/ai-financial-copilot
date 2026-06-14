from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.ai import ChatRequest, ChatResponse
from app.services.financial_analyst import analyze_question

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

    return ChatResponse(
        response=response
    )