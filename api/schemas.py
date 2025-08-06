from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TopProduct(BaseModel):
    product: str
    count: int

class ChannelActivity(BaseModel):
    channel: str
    activity: List[dict]  # e.g., [{"date": "2025-07-16", "count": 10}]

class MessageSearchResult(BaseModel):
    message_id: int
    channel: str
    date: datetime
    message: str
