from fastapi import FastAPI
from fastapi import APIRouter
from api.routes.api import api_router

root_router = APIRouter()
app = FastAPI(title="Meeting Room Occupancy API")

app.include_router(api_router)
app.include_router(root_router)