# utils/date_utils.py
import datetime

def parse_date(date_str):
    if not date_str:
        return datetime.datetime.utcnow()
    try:
        return datetime.datetime.fromisoformat(date_str)
    except ValueError:
        return None
