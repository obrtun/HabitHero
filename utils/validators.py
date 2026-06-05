import re

from exceptions.habit_exceptions import InvalidHabitNameError


def validate_habit_name(name):
    pattern = r"^[A-Za-zА-Яа-я0-9 ]{2,30}$"

    if not re.match(pattern, name):
        raise InvalidHabitNameError(
            "Habit name must be 2-30 characters long and contain only letters, numbers and spaces."
        )