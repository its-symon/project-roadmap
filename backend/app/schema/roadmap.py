from typing import Optional
from pydantic import BaseModel

class RoadmapItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None

class RoadmapItemOut(RoadmapItemBase):
    id: int
    upvotes_count: int

    class Config:
        from_attributes = True
