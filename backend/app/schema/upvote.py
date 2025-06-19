from pydantic import BaseModel

class UpvoteCreate(BaseModel):
    roadmap_item_id: int

class UpvoteOut(BaseModel):
    id: int
    user_id: int
    roadmap_item_id: int

    class Config:
        from_attributes = True
