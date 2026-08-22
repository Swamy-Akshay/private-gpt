from io import BytesIO

from fastapi.testclient import TestClient

from backend.app.main import app

from pathlib import Path

client = TestClient(app)


def test_upload_document():
    response = client.post(
        "/documents/",
        files={
            "file": (
                "test.txt",
                BytesIO(b"Private GPT document test."),
                "text/plain",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "test.txt"
    assert data["content_type"] == "text/plain"
    assert data["extracted_text"] == "Private GPT document test."


def test_get_document():
    upload_response = client.post(
        "/documents/",
        files={
            "file": (
                "test.txt",
                BytesIO(b"Private GPT retrieval test."),
                "text/plain",
            )
        },
    )

    assert upload_response.status_code == 200

    document_id = upload_response.json()["id"]

    response = client.get(
        f"/documents/{document_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == document_id
    assert data["filename"] == "test.txt"
    assert data["extracted_text"] == "Private GPT retrieval test."


def test_get_document_not_found():
    response = client.get("/documents/99999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Document not found."
    }

def test_list_documents():
    first_response = client.post(
        "/documents/",
        files={
            "file": (
                "first.txt",
                BytesIO(b"First document."),
                "text/plain",
            )
        },
    )

    second_response = client.post(
        "/documents/",
        files={
            "file": (
                "second.txt",
                BytesIO(b"Second document."),
                "text/plain",
            )
        },
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    response = client.get("/documents/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 2
    assert data[0]["filename"] == "second.txt"
    assert data[1]["filename"] == "first.txt"

def test_delete_document():
    upload_response = client.post(
        "/documents/",
        files={
            "file": (
                "delete-me.txt",
                BytesIO(b"Document to delete."),
                "text/plain",
            )
        },
    )

    assert upload_response.status_code == 200

    data = upload_response.json()

    document_id = data["id"]
    file_path = data["file_path"]

    response = client.delete(
        f"/documents/{document_id}"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/documents/{document_id}"
    )

    assert get_response.status_code == 404

    assert not Path(file_path).exists()

def test_upload_document_too_large():
    large_file = b"x" * (10 * 1024 * 1024 + 1)

    response = client.post(
        "/documents/",
        files={
            "file": (
                "large.txt",
                BytesIO(large_file),
                "text/plain",
            )
        },
    )

    assert response.status_code == 413

    assert response.json() == {
        "detail": "File is too large. Maximum allowed size is 10 MB."
    }

def test_get_document():
    response = client.post(
        "/documents/",
        files={
            "file": (
                "retrieve.txt",
                b"Document retrieval test.",
                "text/plain",
            )
        },
    )

    assert response.status_code == 200

    document_id = response.json()["id"]

    response = client.get(
        f"/documents/{document_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == document_id
    assert data["filename"] == "retrieve.txt"
    assert data["content_type"] == "text/plain"
    assert data["extracted_text"] == "Document retrieval test."


def test_get_document_not_found():
    response = client.get("/documents/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found."