from datetime import datetime


def parseDatetime(ts, format):
    """
    Parses timestamp to datetime.
    """
    return datetime.strptime(ts, format)