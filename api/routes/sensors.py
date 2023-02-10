from datetime import datetime
from fastapi import APIRouter, HTTPException
from utils.datetime import parseDatetime
from utils.db import pullFromDB

sensors = APIRouter()

@sensors.get('/sensors')
async def getSensors():   
    ## Fetch the list of sensors.
    # The 'set' function is used to eliminate duplicates.
    peopleCounts = pullFromDB()
    return {
        "sensors": set([pc.getSensor() for pc in peopleCounts])
    }

@sensors.get('/sensors/{sensor}/occupancy')
async def getRoomOccupancy(sensor, atInstant: str = None):
    peopleCounts = pullFromDB(sensor)
    if not peopleCounts:
        raise HTTPException(status_code=404, detail=f'Sensor {sensor} is not found.')

    # If the atInstant is none, meaning the parameter is not specified, get the current datetime.
    if atInstant is None:
        atInstant = datetime.now()
    else:
        ## If the param is specified, try to parse it.
        try:
            atInstant = parseDatetime(atInstant, '%Y-%m-%dT%H:%M:%SZ')
        # If the param format is invalid, raise exception.
        except:
            # The HTTP error value 422 indicates that the application received the data but could not process it.
            raise HTTPException(status_code=422, detail='Invalid timestamp format. It should respect the following: year-month-dayThour:minutes:secondsZ.')
    
    # Calculate the sum of count values of the data captured at and before the specifed timestamp.
    sensor_inCount = sum(pc.getInCount() for pc in peopleCounts if pc.getTimeStamp() <= atInstant)
    sensor_outCount = sum(pc.getOutCount() for pc in peopleCounts if pc.getTimeStamp() <= atInstant)

    return {
        "sensor": sensor,
        "inside": sensor_inCount - sensor_outCount
    }
        