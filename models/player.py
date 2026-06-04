from models.stat import Stat


class Player:
    def __init__(self, name):
        self.name = name

        self.stats = {
            "physique": Stat("Physique"),
            "education": Stat("Education"),
            "sociality": Stat("Sociality"),
            "discipline": Stat("Discipline"),
            "creativity": Stat("Creativity")
        }

    def get_stat(self, stat_key):
        return self.stats[stat_key]