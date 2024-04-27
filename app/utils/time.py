from datetime import time

def check_time_slot(open_time, close_time):
    try:
        my_open_time = time.fromisoformat(open_time)
        my_close_time = time.fromisoformat(close_time)
    except ValueError:
        return {"message": "Invalid time format. Please use 'HH:MM:SS'."}, 400

    if my_open_time > my_close_time:
        return {"message": "The open time is later than the close time."}, 400