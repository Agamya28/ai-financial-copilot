from pydantic import BaseModel

class CSVUploadResponse(BaseModel):
    imported_transactions: int
    failed_rows: int