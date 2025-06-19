from enum import Enum
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, or_, func, asc, desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models import RoadmapItem as RoadmapItemModel, Upvote
from app.schema.roadmap import RoadmapItemOut
from app.schema.upvote import UpvoteCreate
from app.dependencies import get_current_user
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
    stmt = (
        select(
            RoadmapItemModel,
            func.count(Upvote.id).label("upvotes_count")
        )
        .outerjoin(Upvote, Upvote.roadmap_item_id == RoadmapItemModel.id)
        .group_by(RoadmapItemModel.id)
    )

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
    rows = result.all()

    roadmap_items = []
    for item, upvote_count in rows:
        roadmap_items.append(RoadmapItemOut(
            id=item.id,
            title=item.title,
            description=item.description,
            category=item.category,
            status=item.status,
            upvotes_count=upvote_count
        ))
    return roadmap_items

@router.get("/roadmaps/popular")
async def get_popular_roadmap_items(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    stmt = (
        select(
            RoadmapItemModel,
            func.count(Upvote.id).label("upvotes_count")
        )
        .outerjoin(Upvote, Upvote.roadmap_item_id == RoadmapItemModel.id)
        .group_by(RoadmapItemModel.id)
    )

    # stmt = stmt.order_by(asc("upvotes_count"))
    stmt = stmt.order_by(desc("upvotes_count"))

    stmt = stmt.limit(limit).offset(offset)

    result = await db.execute(stmt)
    rows = result.all()

    roadmap_items = []
    for item, upvote_count in rows:
        roadmap_items.append(RoadmapItemOut(
            id=item.id,
            title=item.title,
            description=item.description,
            category=item.category,
            status=item.status,
            upvotes_count=upvote_count
        ))
    return roadmap_items

@router.get("/roadmaps/{id}", response_model=RoadmapItemOut)
async def get_roadmap_item(id: int, db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(RoadmapItemModel).where(RoadmapItemModel.id == id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Roadmap does not exits!")
    return item

@router.post("/upvotes/{roadmap_id}", status_code=status.HTTP_201_CREATED)
async def create_upvote(
        roadmap_id: int,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user),
):
    result = await db.execute(select(RoadmapItemModel).where(RoadmapItemModel.id == roadmap_id))
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Roadmap does not exits!")

    upvote = Upvote(
        user_id = current_user.id,
        roadmap_item_id = roadmap_id,
    )
    db.add(upvote)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="You already upvoted this item")

    return {"message": "Upvote successful"}