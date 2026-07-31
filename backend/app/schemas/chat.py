from pydantic import BaseModel


class ChatCreate(BaseModel):
    message: str


class ChatResponse(BaseModel):
    id: int
    message: str

    model_config = {
        "from_attributes": True
    }