import random

from models.enemy import Enemy


class DungeonService:
    def create_enemy(self):
        enemies = [
            Enemy("Goblin", 40, 8),
            Enemy("Skeleton", 55, 10),
            Enemy("Orc", 75, 14)
        ]

        return random.choice(enemies)

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