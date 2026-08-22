from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.schemas.document import DocumentResponse
from backend.app.services.document_service import (
    delete_document,
    get_document,
    list_documents,
    save_document,
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/",
    response_model=DocumentResponse,
    status_code=status.HTTP_200_OK,
)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return save_document(db, file)


@router.get(
    "/",
    response_model=list[DocumentResponse],
    status_code=status.HTTP_200_OK,
)
def get_documents(
    db: Session = Depends(get_db),
):
    return list_documents(db)


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
    status_code=status.HTTP_200_OK,
)
def get_document_by_id(
    document_id: int,
    db: Session = Depends(get_db),
):
    return get_document(db, document_id)


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    delete_document(db, document_id)
    return None