from pathlib import Path

from docx import Document as DocxDocument
from pypdf import PdfReader


def normalize_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]

    return "\n".join(
        line for line in lines
        if line
    )


def extract_text(file_path: str, content_type: str) -> str:
    path = Path(file_path)

    if content_type == "text/plain":
        text = path.read_text(encoding="utf-8")
        return normalize_text(text)

    if content_type == "application/pdf":
        reader = PdfReader(path)

        text = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text.append(page_text)

        return normalize_text("\n".join(text))

    if content_type == (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        document = DocxDocument(path)

        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        )

        return normalize_text(text)

    raise ValueError(
        f"Unsupported content type: {content_type}"
    )