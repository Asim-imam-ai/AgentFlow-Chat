from fastapi import APIRouter
from app.api.routes import health, chat, upload, conversation, history, thread

api_router = APIRouter()

# Include all sub-routers
api_router.include_router(health.router)
api_router.include_router(chat.router)
api_router.include_router(upload.router)
api_router.include_router(conversation.router)
api_router.include_router(history.router)
api_router.include_router(thread.router)
