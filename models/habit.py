class Habit:
    def __init__(
            self,
            name,
            stat_key,
            reward,
            description=""
    ):
        self.name = name
        self.stat_key = stat_key
        self.reward = reward
        self.description = description