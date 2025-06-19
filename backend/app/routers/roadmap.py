from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import get_db
from app.models.roadmap import RoadmapItem as RoadmapItemModel
from app.schema.roadmap import RoadmapItemOut

router = APIRouter()

@router.get("/roadmaps", response_model=List[RoadmapItemOut])
async def get_roadmap_items(db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(RoadmapItemModel))
    items = result.scalars().all()
    return items

@router.get("/roadmaps/{id}", response_model=RoadmapItemOut)
async def get_roadmap_item(id: int, db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(RoadmapItemModel).where(RoadmapItemModel.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Roadmap does not exits!")
    return item