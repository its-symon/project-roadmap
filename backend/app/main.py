from fastapi import FastAPI
from app.routers import auth, roadmap

app = FastAPI()

api_v1_prefix = "/api/v1"

app.include_router(auth.router, prefix=f"{api_v1_prefix}/auth")
app.include_router(roadmap.router, prefix=f"{api_v1_prefix}/roadmap")
# app.include_router(comment.router, prefix=f"{api_v1_prefix}/comments")
