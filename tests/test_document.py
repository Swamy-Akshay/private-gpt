from pathlib import Path

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_upload_txt_document(tmp_path, monkeypatch):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Private GPT test document.", encoding="utf-8")

    response = client.post(
        "/documents/",
        files={
            "file": (
                "test.txt",
                test_file.read_bytes(),
                "text/plain",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "test.txt"
    assert data["content_type"] == "text/plain"

    stored_file = Path(data["file_path"])

    assert stored_file.exists()
    assert stored_file.read_text(encoding="utf-8") == "Private GPT test document."


def test_upload_unsupported_file():
    response = client.post(
        "/documents/",
        files={
            "file": (
                "test.jpg",
                b"fake image data",
                "image/jpeg",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Unsupported file type. Allowed types: TXT, PDF, DOCX."
    )