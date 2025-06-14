from pydantic import BaseModel


class StartRequest(BaseModel):
    """
    Pedantic dialog model from FastApi model
    """
    meet_id: str
