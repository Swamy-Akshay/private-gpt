from pathlib import Path

from docx import Document as DocxDocument

from backend.app.services.document_extractor import (
    extract_text,
    normalize_text,
)


def test_extract_txt(tmp_path):
    file_path = tmp_path / "test.txt"

    file_path.write_text(
        "Private GPT document processing test.",
        encoding="utf-8",
    )

    text = extract_text(
        str(file_path),
        "text/plain",
    )

    assert text == "Private GPT document processing test."


def test_extract_pdf():
    pdf_path = Path("tests/fixtures/sample.pdf")

    text = extract_text(
        str(pdf_path),
        "application/pdf",
    )

    assert "Private GPT" in text


def test_extract_docx(tmp_path):
    file_path = tmp_path / "test.docx"

    document = DocxDocument()
    document.add_paragraph("Private GPT DOCX test.")
    document.save(file_path)

    text = extract_text(
        str(file_path),
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

    assert "Private GPT DOCX test." in text


def test_normalize_text():
    text = "  Hello  \n\n\n  World  "

    result = normalize_text(text)

    assert result == "Hello\nWorld"