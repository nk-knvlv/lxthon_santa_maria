from typing import Optional

from pydantic import BaseModel


class Segment(BaseModel):
    """
    Pedantic dialog model from the Vexa API
    """
    start: float
    end: float
    text: str
    language: str
    created_at: Optional[str] = None
    speaker: Optional[str] = None
    absolute_start_time: str
    absolute_end_time: str
