import datetime

from pydantic import BaseModel


class Segment(BaseModel):
    start: float
    end: float
    text: str
    language: str
    created_at: str
    speaker: str
    absolute_start_time: str
    absolute_end_time: str
