
from datetime import datetime
from zoneinfo import ZoneInfo


def get_datetime():
    try:
        current_time = datetime.now(ZoneInfo("Asia/Kolkata"))

        return {
            "success": True,
            "date": current_time.strftime("%d %B %Y"),
            "day": current_time.strftime("%A"),
            "time": current_time.strftime("%I:%M:%S %p"),
            "timezone": "India Standard Time (IST)"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
