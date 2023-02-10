from models.PeopleCount import PeopleCount
from fastapi import APIRouter
from utils.db import pushToDB

webhook = APIRouter()

@webhook.post('/webhook')
async def webhook_listener(pc: PeopleCount):
    # FastAPI has automatic validation of request data.

    # Insert to database.
    pushToDB(pc)

    # Return HTTP code 200 upon success.
    return {
        "status": 200
    }