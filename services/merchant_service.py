class MerchantService:
    def __init__(self, player):
        self.player = player

    def buy_heal(self):
        if not self.player.spend_gold(1):
            return False

        self.player.heal(30)

        return True

    def buy_damage_bonus(self):
        if not self.player.spend_gold(2):
            return False

        self.player.add_damage_bonus(5)

        return True