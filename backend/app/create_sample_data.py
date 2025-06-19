from app.db import AsyncSessionLocal
from app.models.roadmap import RoadmapItem, Upvote
from app.models.user import User
import random
from datetime import datetime, timedelta
from sqlalchemy import select

async def create_sample_data():
    async with AsyncSessionLocal() as db:
        # Create dummy users if not exist
        existing_users = (await db.execute(select(User))).scalars().all()
        if not existing_users:
            for i in range(1, 6):  # 5 sample users
                user = User(email=f"user{i}@example.com", password_hash="fakehash")
                db.add(user)
            await db.commit()
            existing_users = (await db.execute(select(User))).scalars().all()

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

        created_items = []
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
            created_items.append(item)

        await db.flush()  # So created_items get IDs

        # Add upvotes randomly
        for item in created_items:
            voters = random.sample(existing_users, k=random.randint(1, len(existing_users)))
            for user in voters:
                upvote = Upvote(user_id=user.id, roadmap_item_id=item.id)
                db.add(upvote)

        await db.commit()
        print("Sample data with upvotes created successfully!")
