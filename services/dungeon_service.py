import random

from models.enemy import Enemy


class DungeonService:
    SPECIAL_ATTACK_MANA_COST = 5

    def __init__(self):
        self.enemy_generator = self.generate_enemies()

    def generate_enemies(self):
        enemies = [
            ("Goblin", 40, 8, 1),
            ("Skeleton", 55, 10, 1),
            ("Orc", 75, 14, 2)
        ]

        while True:
            name, hp, attack, coin_reward = random.choice(enemies)
            yield Enemy(name, hp, attack, coin_reward)

    def create_enemy(self):
        return next(self.enemy_generator)

    def calculate_attack_damage(self, player):
        physique = player.get_stat("physique").value
        creativity = player.get_stat("creativity").value

        damage = physique

        critical_chance = creativity

        if random.randint(1, 100) <= critical_chance:
            damage *= 2

        return damage

    def calculate_special_attack_damage(self, player):
        education = player.get_stat("education").value
        physique = player.get_stat("physique").value
        creativity = player.get_stat("creativity").value

        if not player.spend_mana(self.SPECIAL_ATTACK_MANA_COST):
            return None

        damage = physique + education

        critical_chance = creativity

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

    def try_escape(self, player):
        sociality = player.get_stat("sociality").value
        escape_chance = sociality * 2

        return random.randint(1, 100) <= escape_chance