
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import profile, session, user

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(user.router)
app.include_router(session.router)
app.include_router(profile.router)
