from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.csv_upload import CSVUploadResponse
from app.services.csv_import import import_csv_transactions

router = APIRouter(
    prefix="/csv",
    tags=["CSV Upload"]
)

@router.post(
    "/upload",
    response_model=CSVUploadResponse
)
def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed."
        )
    return import_csv_transactions(
        file=file,
        db=db,
        user_id=current_user.id
    )

