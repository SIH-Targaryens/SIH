from datetime import datetime

def get_current_time_iso():
    return datetime.utcnow().isoformat() + "Z"