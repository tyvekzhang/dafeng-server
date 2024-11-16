from datetime import datetime


def get_current_time(fmt: str = "%Y-%m-%d %H:%M:%S"):
    now = datetime.now()
    now_str = now.strftime(fmt)
    now_str = now_str.replace(" ", "_")
    return now_str
