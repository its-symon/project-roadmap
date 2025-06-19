from app.db import AsyncSessionLocal
from app.models.roadmap import RoadmapItem
import random
from datetime import datetime, timedelta


async def create_sample_data():
    async with AsyncSessionLocal() as db:
        sample_items = [
            ("Dark Mode Support", "Implement dark theme across the application", "Frontend", "Planning"),
            ("User Authentication", "JWT-based authentication system", "Security", "Completed"),
            ("Mobile App", "Native mobile application", "Mobile", "In Progress"),
            ("Payment System", "Stripe payment integration", "Integration", "Testing"),
            ("Real-time Features", "WebSocket implementation", "Backend", "Planning"),
            ("Admin Panel", "Administrative dashboard", "Frontend", "Under Review"),
            ("API Security", "Rate limiting and security measures", "Security", "Planning"),
            ("File Management", "File upload and management system", "Backend", "In Progress"),
            ("Notifications", "Email and push notifications", "Integration", "Completed"),
            ("Search Engine", "Advanced search functionality", "Backend", "On Hold")
        ]

        for title, description, category, status in sample_items:
            days_ago = random.randint(1, 90)
            created_at = datetime.now() - timedelta(days=days_ago)

            item = RoadmapItem(
                title=title,
                description=description,
                category=category,
                status=status,
                created_at=created_at
            )
            db.add(item)

        await db.commit()
        print("Sample data created successfully!")



