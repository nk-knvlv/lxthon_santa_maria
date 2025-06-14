from typing import Optional, List

from pydantic import BaseModel

from model.segment import Segment


class ResponseVexa(BaseModel):
    """
    Pydantic call model from Vexa API
    """
    id: int
    platform: str
    native_meeting_id: str
    constructed_meeting_url: str
    status: str
    start_time: Optional[str] = None
    end_time: Optional[str]
    segments: List[Segment]
