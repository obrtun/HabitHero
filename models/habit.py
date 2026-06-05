class Habit:
    def __init__(self, name, stat_key, reward):
        self.name = name
        self.stat_key = stat_key
        self.reward = reward
        self.last_completed_date = None

    def to_dict(self):
        return {
            "name": self.name,
            "stat_key": self.stat_key,
            "reward": self.reward,
            "last_completed_date": self.last_completed_date
        }

    @classmethod
    def from_dict(cls, data):
        habit = cls(
            data["name"],
            data["stat_key"],
            data["reward"]
        )

        habit.last_completed_date = data["last_completed_date"]

        return habit