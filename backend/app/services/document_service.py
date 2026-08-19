from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from backend.app.models.document import Document


UPLOAD_DIR = Path("storage/documents")

ALLOWED_CONTENT_TYPES = {
    "text/plain": ".txt",
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
}


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

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    extension = ALLOWED_CONTENT_TYPES[file.content_type]
    stored_filename = f"{uuid4().hex}{extension}"
    file_path = UPLOAD_DIR / stored_filename

    with file_path.open("wb") as buffer:
        buffer.write(file.file.read())

    document = Document(
        filename=file.filename,
        file_path=str(file_path),
        content_type=file.content_type,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document