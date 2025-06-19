from fastapi import FastAPI
from app.routers import auth, roadmap
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import Base, engine
from app.routers import auth, roadmap

app = FastAPI()

api_v1_prefix = "/api/v1"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables at startup
    print("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created.")
    yield

app.router.lifespan_context = lifespan

app.include_router(auth.router, prefix=f"{api_v1_prefix}/auth")
app.include_router(roadmap.router, prefix=f"{api_v1_prefix}/roadmap")
# app.include_router(comment.router, prefix=f"{api_v1_prefix}/comments")

@app.get("/")
async def root():
    return {"message": "Roadmap API is running!"}
