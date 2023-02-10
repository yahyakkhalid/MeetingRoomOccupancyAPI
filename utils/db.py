import pickle
from models.PeopleCount import PeopleCount


def pushToDB(pc: PeopleCount):
    """
    Reads the array of Objects. Appends a new Object and write the array back.
    """
    db = []
    with open('.db', 'rb') as db_file:
        # The '.db' might be empty.
        try:
            db = pickle.load(db_file)
        except:
            db = []

    db.append(pc)
    with open('.db', 'wb') as db_file:
        pickle.dump(db, db_file)

def pullFromDB(sensor = None):
    """
    Returns only the objects for the specified sensor.
    Returns all objects if the sensor is not specified.
    """
    with open('.db', 'rb') as db_file:
        # The '.db' might be empty.
        try:
            db = pickle.load(db_file)
        except:
            db = []
        return [pc for pc in db if pc.getSensor() == sensor] if sensor else db