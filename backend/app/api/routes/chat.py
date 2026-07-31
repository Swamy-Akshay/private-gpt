from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.models.chat import Chat
from backend.app.schemas.chat import ChatCreate, ChatResponse
from backend.app.services import chat_service

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
def create_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    return chat_service.create_chat(db, chat)

from typing import List

@router.get("", response_model=List[ChatResponse])
def get_all_chats(db: Session = Depends(get_db)):
    return chat_service.get_all_chats(db)

@router.get("/{chat_id}", response_model=ChatResponse)
def get_chat(chat_id: int, db: Session = Depends(get_db)):
    chat = chat_service.get_chat(db, chat_id)

    if chat is None:
        raise HTTPException(
            status_code=404,
            detail="Chat not found",
        )

    return chat

@router.put("/{chat_id}", response_model=ChatResponse)
def update_chat(
    chat_id: int,
    chat_data: ChatCreate,
    db: Session = Depends(get_db),
):
    chat = chat_service.update_chat(db, chat_id, chat_data)

    if chat is None:
        raise HTTPException(
            status_code=404,
            detail="Chat not found",
        )

    return chat

@router.delete("/{chat_id}")
def delete_chat(chat_id: int, db: Session = Depends(get_db)):
    deleted = chat_service.delete_chat(db, chat_id)

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Chat not found",
        )

    return {
        "message": "Chat deleted successfully"
    }