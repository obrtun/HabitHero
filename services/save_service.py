import json
import os

from models.player import Player
from models.habit import Habit


class SaveService:
    def __init__(self, file_path="data/save.json"):
        self.file_path = file_path

    def save(self, player, habits):
        os.makedirs("data", exist_ok=True)

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                {
                    "player": player.to_dict(),
                    "habits": [habit.to_dict() for habit in habits]
                },
                file,
                indent=4,
                ensure_ascii=False
            )

    def load(self):
        if not os.path.exists(self.file_path):
            return None

        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return (
            Player.from_dict(data["player"]),
            [Habit.from_dict(habit) for habit in data["habits"]]
        )