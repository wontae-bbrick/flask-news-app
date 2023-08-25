from datetime import datetime

def type_datetime(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError("Invalid datetime format. Use YYYY-MM-DD HH:MM:SS.")