from dataclasses import dataclass
from datetime import datetime
from utils.datetime import parseDatetime

@dataclass
class PeopleCount:
    sensor: str
    ts: datetime
    in_count: int
    out_count: int

    def __init__(self, sensor, ts, in_count, out_count):
        self.sensor = sensor
        self.ts = parseDatetime(ts, '%Y-%m-%dT%H:%M:%SZ')
        self.in_count = in_count
        self.out_count = out_count
    
    def getSensor(self):
        return self.sensor
    
    def getTimeStamp(self):
        return self.ts
    
    def getInCount(self):
        return self.in_count

    def getOutCount(self):
        return self.out_count

