from typing import List
from fastapi import APIRouter, HTTPException, Depends, Request, Query
from fastapi_sa_orm_filter.main import FilterCore
from fastapi_sa_orm_filter.operators import Operators as ops
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import get_db
from app.models.roadmap import RoadmapItem as RoadmapItemModel
from app.schema.roadmap import RoadmapItemOut

router = APIRouter()

object_filter = {
    'title': [ops.eq, ops.in_, ops.like, ops.startswith, ops.contains],
    'category': [ops.eq, ops.in_],
    'status': [ops.eq, ops.in_]
}

@router.get("/roadmaps", response_model=List[RoadmapItemOut])
async def get_roadmap_items(
    filter_query: str = Query(default='', description="Filter query string"),
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page")
):
    filter_inst = FilterCore(RoadmapItemModel, object_filter)
    
    # Get the filtered query using the correct method
    if filter_query:
        # Apply filters using the filter_query string
        base_query = filter_inst.get_query(filter_query)
    else:
        # No filters, just select all
        base_query = select(RoadmapItemModel)
    
    # Always apply default ordering
    base_query = base_query.order_by(RoadmapItemModel.created_at.desc())
    
    # Apply pagination
    offset = (page - 1) * size
    base_query = base_query.offset(offset).limit(size)
    
    result = await db.execute(base_query)
    items = result.scalars().all()
    return items

# @router.get("/roadmaps/popular", response_model=List[RoadmapItemOut])
# async def get_popular_roadmaps(db: AsyncSession = Depends(get_db)):
#     query = select(RoadmapItemModel).join(Upvote).group_by(RoadmapItemModel.id).order_by(func.count(Upvote.id).desc())
#     result = await db.execute(query)
#     return result.scalars().all()

@router.get("/roadmaps/{id}", response_model=RoadmapItemOut)
async def get_roadmap_item(id: int, db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(RoadmapItemModel).where(RoadmapItemModel.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Roadmap does not exits!")
    return item