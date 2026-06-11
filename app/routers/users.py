from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user, get_users

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

from app.crud.user import (
    create_user,
    get_users,
    get_user_by_email
)

@router.post("/", response_model=UserResponse)
def create_user_route(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = get_user_by_email(
        db,
        user.email
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    return create_user(db, user)


@router.get("/", response_model=list[UserResponse])
def get_users_route(
    db: Session = Depends(get_db)
):
    return get_users(db)