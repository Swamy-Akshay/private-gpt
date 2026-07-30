from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def home():
    return {"message": "Welcome to Private GPT!"}

@router.get("/error")
def error():
    raise Exception("Testing")