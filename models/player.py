from models.stat import Stat


class Player:
    def __init__(self, name):
        self.name = name
        self.max_hp = 100
        self.current_hp = self.max_hp
        self.stats = {
            "physique": Stat("Physique"),
            "education": Stat("Education"),
            "sociality": Stat("Sociality"),
            "discipline": Stat("Discipline"),
            "creativity": Stat("Creativity")
        }

    def get_stat(self, stat_key):
        return self.stats[stat_key]

    def to_dict(self):
        return {
            "name": self.name,
            "stats": {
                key: stat.to_dict()
                for key, stat in self.stats.items()
            }
        }

    def take_damage(self, damage):
        self.current_hp -= damage

        if self.current_hp < 0:
            self.current_hp = 0

    def is_alive(self):
        return self.current_hp > 0

    def restore_hp(self):
        self.current_hp = self.max_hp

    @classmethod
    def from_dict(cls, data):
        player = cls(data["name"])

        player.stats = {
            key: Stat.from_dict(stat_data)
            for key, stat_data in data["stats"].items()
        }

        return player