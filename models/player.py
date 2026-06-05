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

        self.gold = 0
        self.damage_bonus = 0

        self.max_hp = 100
        self.current_hp = self.max_hp
        self.max_mana = self.get_max_mana()
        self.current_mana = self.max_mana

    def get_stat(self, stat_key):
        return self.stats[stat_key]

    def get_max_mana(self):
        return self.get_stat("education").value * 2

    def restore_combat_resources(self):
        self.max_hp = 100 + self.get_stat("physique").value * 2
        self.current_hp = self.max_hp

        self.max_mana = self.get_max_mana()
        self.current_mana = self.max_mana

        self.gold = 0
        self.damage_bonus = 0

    def spend_mana(self, amount):
        if self.current_mana < amount:
            return False

        self.current_mana -= amount
        return True

    def take_damage(self, damage):
        self.current_hp -= damage

        if self.current_hp < 0:
            self.current_hp = 0

    def heal(self, amount):
        self.current_hp += amount

        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

    def is_alive(self):
        return self.current_hp > 0

    def add_gold(self, amount):
        self.gold += amount

    def spend_gold(self, amount):
        if self.gold < amount:
            return False

        self.gold -= amount
        return True

    def add_damage_bonus(self, amount):
        self.damage_bonus += amount

    def to_dict(self):
        return {
            "name": self.name,
            "stats": {
                key: stat.to_dict()
                for key, stat in self.stats.items()
            }
        }

    @classmethod
    def from_dict(cls, data):
        player = cls(data["name"])

        player.stats = {
            key: Stat.from_dict(stat_data)
            for key, stat_data in data["stats"].items()
        }

        player.restore_combat_resources()

        return player