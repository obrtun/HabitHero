import re


def validate_habit_name(name):
    pattern = r"^[A-Za-zА-Яа-я0-9 ]{2,30}$"

    return re.match(pattern, name) is not None