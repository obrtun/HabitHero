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

    def generate_event(self):
        return random.choice([
            "combat",
            "combat",
            "combat",
            "merchant"
        ])

    def create_enemy(self):
        return next(self.enemy_generator)

    def calculate_attack_damage(self, player):
        damage = player.get_stat("physique").value
        critical_chance = player.get_stat("creativity").value

        if random.randint(1, 100) <= critical_chance:
            damage *= 2

        return damage + player.damage_bonus

    def calculate_special_attack_damage(self, player):
        if not player.spend_mana(self.SPECIAL_ATTACK_MANA_COST):
            return None

        damage = (
            player.get_stat("physique").value
            + player.get_stat("education").value
        )

        critical_chance = player.get_stat("creativity").value

        if random.randint(1, 100) <= critical_chance:
            damage *= 2

        return damage + player.damage_bonus

    def calculate_enemy_damage(self, player, enemy):
        defense = player.get_stat("discipline").value // 3
        damage = enemy.attack - defense

        return max(damage, 1)

    def try_escape(self, player):
        escape_chance = player.get_stat("sociality").value * 2
        return random.randint(1, 100) <= escape_chance