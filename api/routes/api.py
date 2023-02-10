from fastapi import APIRouter
from .sensors import sensors
from .webhook import webhook

api_router = APIRouter()

api_router.include_router(sensors, prefix="/api")
api_router.include_router(webhook, prefix="/api")
