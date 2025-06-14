from pydantic import BaseModel


class StartRequest(BaseModel):
    meet_id: str
