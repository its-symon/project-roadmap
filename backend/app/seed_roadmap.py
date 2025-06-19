from app.db import SessionLocal
from app.models.roadmap import RoadmapItem

roadmaps = [
    {"title": "Add Dark Mode", "description": "Implement dark mode support", "category": "UI", "status": "Planned", "upvotes": 10},
    {"title": "Real-time Chat", "description": "Enable real-time discussion", "category": "Feature", "status": "In Progress", "upvotes": 20},
    {"title": "Export to PDF", "description": "Allow roadmap export as PDF", "category": "Tooling", "status": "Completed", "upvotes": 35},
]

db = SessionLocal()
for data in roadmaps:
    db.add(RoadmapItem(**data))

db.commit()
db.close()