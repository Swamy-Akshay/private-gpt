from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.session import get_db

router = APIRouter()


@router.get("/")
def home(db: Session = Depends(get_db)):
    return {
        "message": "Welcome to Private GPT!",
        "database": "connected"
    }