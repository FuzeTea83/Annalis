import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from config import settings
from core.middleware import setup_exception_handlers
from database import engine, Base
from routers import auth_router, documents_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Annalis API", version="1.0.0", prefix="/api")

# noinspection bad-argument-type
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(documents_router)

if not os.path.exists("documents"):
    os.makedirs("documents")
if os.path.exists("documents"):
    app.mount("/documents", StaticFiles(directory="documents"), name="documents")

setup_exception_handlers(app)
