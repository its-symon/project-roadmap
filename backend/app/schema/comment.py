from __future__ import annotations
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    parent_id: Optional[int] = None  # For replies

class CommentOut(CommentBase):
    id: int
    user_id: int
    roadmap_item_id: int
    parent_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    replies: List[CommentOut] = []  # recursive type hint

    class Config:
        from_attributes = True
