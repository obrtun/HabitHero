class Enemy:
    def __init__(self, name, hp, attack, coin_reward=1):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.coin_reward = coin_reward

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage

        if self.hp < 0:
            self.hp = 0