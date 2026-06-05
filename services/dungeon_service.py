import random

from models.enemy import Enemy


class DungeonService:
    def __init__(self):
        self.enemy_generator = self.generate_enemies()

    def generate_enemies(self):
        enemies = [
            ("Goblin", 40, 8),
            ("Skeleton", 55, 10),
            ("Orc", 75, 14)
        ]

        while True:
            name, hp, attack = random.choice(enemies)
            yield Enemy(name, hp, attack)

    def create_enemy(self):
        return next(self.enemy_generator)

    def calculate_player_damage(self, player):
        physique = player.get_stat("physique").value
        education = player.get_stat("education").value

        damage = physique

        critical_chance = education

        if random.randint(1, 100) <= critical_chance:
            damage *= 2

        return damage

    def calculate_enemy_damage(self, player, enemy):
        discipline = player.get_stat("discipline").value

        defense = discipline // 3
        damage = enemy.attack - defense

        if damage < 1:
            damage = 1

        return damage