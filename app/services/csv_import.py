import csv
from io import StringIO
from datetime import datetime

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.database.models import Transaction

def import_csv_transactions(
    file: UploadFile,
    db: Session,
    user_id: int
) -> dict:
    content = file.file.read().decode("utf-8")

    csv_reader = csv.DictReader(
        StringIO(content)
    )

    imported_transactions = 0
    failed_rows = 0

    for row in csv_reader:
        try:
            transaction = Transaction(
                amount=row["amount"],
                category=row["category"].strip().title(),
                description=row["description"],
                merchant=row["merchant"],
                transaction_date=datetime.strptime(
                    row["transaction_date"],
                    "%Y-%m-%d"
                ).date(),
                user_id=user_id
            )

            db.add(transaction)

            imported_transactions += 1
            db.commit()
        except Exception:
            db.rollback()
            failed_rows += 1

    

    return {
        "imported_transactions": imported_transactions,
        "failed_rows": failed_rows
    }