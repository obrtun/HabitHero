import tkinter as tk
import random


class DungeonWindow:
    def __init__(self, root, player, dungeon_service):
        self.root = root
        self.player = player
        self.dungeon_service = dungeon_service
        self.enemy = None

        self.player.restore_combat_resources()

        self.window = tk.Toplevel(self.root)
        self.window.title("Dungeon")
        self.window.geometry("520x450")
        self.window.resizable(False, False)

        self.create_widgets()
        self.next_room()

    def create_widgets(self):
        tk.Label(
            self.window,
            text="Dungeon",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        self.player_label = tk.Label(
            self.window,
            text="",
            font=("Arial", 12)
        )
        self.player_label.pack(pady=5)

        self.enemy_label = tk.Label(
            self.window,
            text="",
            font=("Arial", 14)
        )
        self.enemy_label.pack(pady=10)

        self.status_label = tk.Label(
            self.window,
            text="",
            font=("Arial", 11),
            wraplength=450
        )
        self.status_label.pack(pady=15)

        self.buttons_frame = tk.Frame(self.window)
        self.buttons_frame.pack(pady=10)

        self.attack_button = tk.Button(
            self.buttons_frame,
            text="Attack",
            width=14,
            command=self.attack_enemy
        )
        self.attack_button.pack(side="left", padx=5)

        self.special_attack_button = tk.Button(
            self.buttons_frame,
            text="Special Attack",
            width=14,
            command=self.special_attack
        )
        self.special_attack_button.pack(side="left", padx=5)

        self.run_button = tk.Button(
            self.buttons_frame,
            text="Run",
            width=14,
            command=self.run_away
        )
        self.run_button.pack(side="left", padx=5)

        self.next_room_button = tk.Button(
            self.window,
            text="Next Room",
            width=14,
            command=self.next_room
        )
        self.next_room_button.pack(pady=5)

    def update_info(self):
        self.player_label.config(
            text=(
                f"HP: {self.player.current_hp}/{self.player.max_hp} | "
                f"Mana: {self.player.current_mana}/{self.player.max_mana} | "
                f"Coins: {self.player.gold} | "
                f"Damage bonus: +{self.player.damage_bonus}"
            )
        )

        if self.enemy:
            self.enemy_label.config(
                text=f"{self.enemy.name}\nHP: {self.enemy.hp}"
            )

    def next_room(self):
        event = random.choice(["combat", "combat", "merchant"])

        if event == "combat":
            self.start_combat()
        else:
            self.show_merchant()

    def start_combat(self):
        self.enemy = self.dungeon_service.create_enemy()

        self.enemy_label.config(
            text=f"{self.enemy.name}\nHP: {self.enemy.hp}"
        )

        self.status_label.config(
            text=f"You enter a room. {self.enemy.name} appears!"
        )

        self.attack_button.config(
            text="Attack",
            state="normal",
            command=self.attack_enemy
        )
        self.special_attack_button.config(
            text="Special Attack",
            state="normal",
            command=self.special_attack
        )
        self.run_button.config(
            text="Run",
            state="normal",
            command=self.run_away
        )

        self.next_room_button.config(state="disabled")

        self.update_info()

    def show_merchant(self):
        self.enemy = None

        self.enemy_label.config(text="Merchant")

        self.status_label.config(
            text="A merchant offers you supplies."
        )

        self.attack_button.config(
            text="Buy Heal (1)",
            state="normal",
            command=self.buy_heal
        )
        self.special_attack_button.config(
            text="Buy Damage (2)",
            state="normal",
            command=self.buy_damage_bonus
        )
        self.run_button.config(
            text="Leave",
            state="normal",
            command=self.next_room
        )

        self.next_room_button.config(state="normal")

        self.update_info()

    def buy_heal(self):
        if not self.player.spend_gold(1):
            self.status_label.config(text="Not enough coins.")
            return

        self.player.heal(30)
        self.update_info()
        self.status_label.config(text="You bought healing. +30 HP.")

    def buy_damage_bonus(self):
        if not self.player.spend_gold(2):
            self.status_label.config(text="Not enough coins.")
            return

        self.player.add_damage_bonus(5)
        self.update_info()
        self.status_label.config(text="You bought damage bonus. +5 damage.")

    def enemy_turn(self):
        enemy_damage = self.dungeon_service.calculate_enemy_damage(
            self.player,
            self.enemy
        )

        self.player.take_damage(enemy_damage)

        if not self.player.is_alive():
            self.update_info()
            self.status_label.config(
                text=f"{self.enemy.name} dealt {enemy_damage} damage. You were defeated!"
            )
            self.disable_combat_buttons()
            self.next_room_button.config(state="disabled")
            return False

        return enemy_damage

    def attack_enemy(self):
        damage = self.dungeon_service.calculate_attack_damage(self.player)
        damage += self.player.damage_bonus

        self.enemy.take_damage(damage)

        if not self.enemy.is_alive():
            self.handle_victory(damage)
            return

        enemy_damage = self.enemy_turn()
        self.update_info()

        if enemy_damage is not False:
            self.status_label.config(
                text=f"You attacked for {damage} damage. {self.enemy.name} dealt {enemy_damage} damage."
            )

    def special_attack(self):
        damage = self.dungeon_service.calculate_special_attack_damage(
            self.player
        )

        if damage is None:
            self.status_label.config(
                text="Not enough mana for special attack."
            )
            return

        damage += self.player.damage_bonus
        self.enemy.take_damage(damage)

        if not self.enemy.is_alive():
            self.handle_victory(damage)
            return

        enemy_damage = self.enemy_turn()
        self.update_info()

        if enemy_damage is not False:
            self.status_label.config(
                text=f"You used special attack for {damage} damage. {self.enemy.name} dealt {enemy_damage} damage."
            )

    def run_away(self):
        if self.dungeon_service.try_escape(self.player):
            self.status_label.config(
                text="You successfully escaped from combat."
            )
            self.disable_combat_buttons()
            self.next_room_button.config(state="normal")
            return

        enemy_damage = self.enemy_turn()
        self.update_info()

        if enemy_damage is not False:
            self.status_label.config(
                text=f"Escape failed! {self.enemy.name} dealt {enemy_damage} damage."
            )

    def handle_victory(self, damage):
        self.player.add_gold(self.enemy.coin_reward)
        self.update_info()

        self.status_label.config(
            text=(
                f"You dealt {damage} damage. "
                f"You defeated {self.enemy.name}! "
                f"+{self.enemy.coin_reward} coin."
            )
        )

        self.disable_combat_buttons()
        self.next_room_button.config(state="normal")

    def disable_combat_buttons(self):
        self.attack_button.config(state="disabled")
        self.special_attack_button.config(state="disabled")
        self.run_button.config(state="disabled")