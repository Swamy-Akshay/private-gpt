from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_path: str
    content_type: str
    created_at: datetime
    extracted_text: str | None = None

    model_config = ConfigDict(from_attributes=True)