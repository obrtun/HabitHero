class FightService:
    def __init__(self, player, dungeon_service):
        self.player = player
        self.dungeon_service = dungeon_service

    def attack(self, enemy):
        damage = self.dungeon_service.calculate_attack_damage(self.player)
        enemy.take_damage(damage)
        return damage

    def special_attack(self, enemy):
        damage = self.dungeon_service.calculate_special_attack_damage(self.player)

        if damage is None:
            return None

        enemy.take_damage(damage)
        return damage

    def enemy_attack(self, enemy):
        damage = self.dungeon_service.calculate_enemy_damage(
            self.player,
            enemy
        )
        self.player.take_damage(damage)
        return damage

    def try_escape(self):
        return self.dungeon_service.try_escape(self.player)

    def victory(self, enemy):
        self.player.add_gold(enemy.coin_reward)