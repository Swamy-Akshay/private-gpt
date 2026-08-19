from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.schemas.document import DocumentResponse
from backend.app.services.document_service import save_document


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post("/", response_model=DocumentResponse)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return save_document(db, file)