from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db import Base


class RoadmapItem(Base):
    __tablename__ = "roadmap_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    status = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    comments = relationship("Comment", back_populates="roadmap_item", cascade="all, delete-orphan")
    upvotes = relationship("Upvote", back_populates="roadmap_item", cascade="all, delete-orphan")

class Upvote(Base):
    __tablename__ = "upvotes"
    __table_args__ = (
        UniqueConstraint('user_id', 'roadmap_item_id', name='unique_user_roadmap_upvote'),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    roadmap_item_id = Column(Integer, ForeignKey("roadmap_items.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="upvotes")
    roadmap_item = relationship("RoadmapItem", back_populates="upvotes")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    roadmap_item_id = Column(Integer, ForeignKey("roadmap_items.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)

    user = relationship("User", back_populates="comments")
    roadmap_item = relationship("RoadmapItem", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], backref="replies")

    def nesting_level(self):
        level = 0
        current = self
        while current.parent:
            level += 1
            current = current.parent
        return level