from datetime import datetime, time

class TimeService:
    @staticmethod
    def get_current_time():
        return datetime.now()

    def check_time_slot(open_time, close_time):
        try:
            my_open_time = time.fromisoformat(open_time)
            my_close_time = time.fromisoformat(close_time)
        except ValueError:
            return {"message": "Invalid time format. Please use 'HH:MM:SS'."}, 400

        if my_open_time > my_close_time:
            return {"message": "The open time is later than the close time."}, 400
        return {"message": "Time slot is legal."}, 200

    def check_time_overlap(start_time1, end_time1, start_time2, end_time2):
        if end_time1 <= start_time2:
            return False
        if end_time2 <= start_time1:
            return False
        return True