from sqlalchemy.orm import Session

from backend.app.models.chat import Chat
from backend.app.schemas.chat import ChatCreate


def create_chat(db: Session, chat_data: ChatCreate) -> Chat:
    new_chat = Chat(message=chat_data.message)

    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)

    return new_chat


def get_all_chats(db: Session):
    return db.query(Chat).all()


def get_chat(db: Session, chat_id: int):
    return db.query(Chat).filter(Chat.id == chat_id).first()


def update_chat(db: Session, chat_id: int, chat_data: ChatCreate):
    chat = get_chat(db, chat_id)

    if chat is None:
        return None

    chat.message = chat_data.message

    db.commit()
    db.refresh(chat)

    return chat


def delete_chat(db: Session, chat_id: int):
    chat = get_chat(db, chat_id)

    if chat is None:
        return None

    db.delete(chat)
    db.commit()

    return True