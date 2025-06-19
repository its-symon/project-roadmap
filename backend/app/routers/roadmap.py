from enum import Enum
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models import RoadmapItem as RoadmapItemModel
from app.schema.roadmap import RoadmapItemOut
from app.db import get_db
router = APIRouter()

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

@router.get("/roadmaps", response_model=List[RoadmapItemOut])
async def get_roadmap_items(
    status: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    sort: Optional[SortOrder] = Query(None, description="Sort by title: asc or desc"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(RoadmapItemModel)

    if status:
        stmt = stmt.where(RoadmapItemModel.status == status)
    if category:
        stmt = stmt.where(RoadmapItemModel.category == category)
    if search:
        stmt = stmt.where(
            or_(
                RoadmapItemModel.title.ilike(f"%{search}%"),
                RoadmapItemModel.description.ilike(f"%{search}%")
            )
        )

    # Apply sorting by title if requested
    if sort == SortOrder.asc:
        stmt = stmt.order_by(RoadmapItemModel.title.asc())
    elif sort == SortOrder.desc:
        stmt = stmt.order_by(RoadmapItemModel.title.desc())

    stmt = stmt.limit(limit).offset(offset)

    result = await db.execute(stmt)
    items = result.scalars().all()
    return items

# @router.get("/roadmaps/popular")
# async def get_popular_roadmap_items(
#     limit: int = Query(10, ge=1, le=100),
#     offset: int = Query(0, ge=0),
#     db: AsyncSession = Depends(get_db)
# ):
#     total_stmt = (
#         select(func.count(RoadmapItemModel.id))
#         .select_from(RoadmapItemModel)
#     )
#     total = (await db.execute(total_stmt)).scalar()
#
#     # Main query with upvote count
#     stmt = (
#         select(
#             RoadmapItemModel,
#             func.count(Upvote.id).label("upvote_count")
#         )
#         .outerjoin(Upvote, Upvote.roadmap_item_id == RoadmapItemModel.id)
#         .group_by(RoadmapItemModel.id)
#         .order_by(desc("upvote_count"))
#         .limit(limit)
#         .offset(offset)
#     )
#
#     result = await db.execute(stmt)
#     rows = result.all()
#
#     # Unpack RoadmapItem and upvote_count
#     items = []
#     for item, upvote_count in rows:
#         item_dict = RoadmapItemOut.from_orm(item).dict()
#         item_dict["upvote_count"] = upvote_count
#         items.append(item_dict)
#
#     return {"total": total, "items": items}

@router.get("/roadmaps/{id}", response_model=RoadmapItemOut)
async def get_roadmap_item(id: int, db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(RoadmapItemModel).where(RoadmapItemModel.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Roadmap does not exits!")
    return item