from datetime import datetime
import os


def log_habit_completion(func):
    def wrapper(self, player, habit):
        os.makedirs("data", exist_ok=True)

        with open("data/habit_history.log", "a", encoding="utf-8") as file:
            file.write(
                f"{datetime.now()} - {habit.name} completed\n"
            )

        return func(self, player, habit)

    return wrapper