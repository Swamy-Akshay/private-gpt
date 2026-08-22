from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from backend.app.models.document import Document
from backend.app.services.document_extractor import extract_text


UPLOAD_DIR = Path("storage/documents")

ALLOWED_CONTENT_TYPES = {
    "text/plain": ".txt",
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
}

MAX_FILE_SIZE = 10 * 1024 * 1024


def save_document(
    db: Session,
    file: UploadFile,
) -> Document:
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required.",
        )

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Allowed types: TXT, PDF, DOCX.",
        )

    content = file.file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail="File is too large. Maximum allowed size is 10 MB.",
        )

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    extension = ALLOWED_CONTENT_TYPES[file.content_type]
    stored_filename = f"{uuid4().hex}{extension}"
    file_path = UPLOAD_DIR / stored_filename

    with file_path.open("wb") as buffer:
        buffer.write(content)

    extracted_text = extract_text(
        str(file_path),
        file.content_type,
    )

    document = Document(
        filename=file.filename,
        file_path=str(file_path),
        content_type=file.content_type,
        extracted_text=extracted_text,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def get_document(
    db: Session,
    document_id: int,
) -> Document:
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    return document


def list_documents(
    db: Session,
) -> list[Document]:
    return (
        db.query(Document)
        .order_by(Document.id.desc())
        .all()
    )


def delete_document(
    db: Session,
    document_id: int,
) -> None:
    document = get_document(db, document_id)

    file_path = Path(document.file_path)

    if file_path.exists():
        file_path.unlink()

    db.delete(document)
    db.commit()