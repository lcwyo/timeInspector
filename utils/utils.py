import re
from datetime import datetime, timedelta
import os
from PyQt5.QtGui import QPixmap


def parse_time(time_str: str) -> datetime:
    """Parses a time string and returns a datetime object."""
    try:
        return datetime.strptime(time_str, '%H:%M')
    except ValueError:
        return None


def calculate_time_difference(start_time: datetime, end_time: datetime) -> timedelta:
    """Returns the difference between two times as a timedelta object."""
    return end_time - start_time


def calculate_go_home_time(start_time: datetime, hours: int = 8, minutes: int = 50) -> str:
    """Calculates the time when the user can leave the building."""
    if not isinstance(start_time, datetime):
        raise ValueError("start_time must be a datetime.datetime object")
    
    end_time = start_time + timedelta(hours=hours, minutes=minutes)
    return end_time.strftime('%H:%M')


from datetime import datetime, timedelta

def calculate_time_worked_before_lunch(start_time: datetime, lunch_start: datetime) -> timedelta:
    """Calculates the time worked before the lunch break."""
    if lunch_start <= start_time:
        raise ValueError("Lunch start time must be after start time.")
    return lunch_start - start_time

def calculate_remaining_working_hours(time_worked_before_lunch: timedelta, lunch_duration: timedelta) -> timedelta:
    """Calculates the remaining working hours after the lunch break."""
    required_work_time = timedelta(hours=8, minutes=00)  # Fixed required working time
    
    # Subtract the time worked before lunch and lunch duration from the required work time
    remaining_work_time = required_work_time - time_worked_before_lunch

    # Ensure the remaining work time is not negative
    if remaining_work_time < timedelta(0):
        raise ValueError("Invalid lunch duration. Remaining work time cannot be negative.")
    
    return remaining_work_time

def calculate_go_home_time_with_lunch(remaining_work_time: timedelta, lunch_end: datetime) -> str:
    """Calculates the time to go home after accounting for the lunch break."""
    go_home_time = lunch_end + remaining_work_time
    return go_home_time.strftime('%H:%M')



def get_default_time() -> str:
    """Returns the default time in the format '8:00'."""
    return "8:00"


def get_current_time() -> str:
    """Returns the current time in the format 'HH:MM'."""
    return datetime.now().strftime('%H:%M')


def get_time_left(time_on: timedelta) -> timedelta:
    """Returns the time left until the user can clock out."""
    return timedelta(hours=7, minutes=50) - time_on


def get_image_path(image_name: str) -> str:
    """Returns the path to an image based on the image name."""
    return os.path.join(os.getcwd(), "assets", image_name)


def validate_time_input(time_str):
    """Returns True if the input time string is in valid format (HH:MM), False otherwise."""
    try:
        datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False

def load_image(self, image_name: str):
    """Loads and returns an image based on the name provided."""
    image_path = get_image_path(image_name)
    if not os.path.exists(image_path):
        self.show_error_message(f"Image '{image_name}' not found.")
        return None
    pixmap = QPixmap(image_path)
    return pixmap
