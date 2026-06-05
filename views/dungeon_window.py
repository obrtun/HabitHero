import tkinter as tk

from services.fight_service import FightService
from services.merchant_service import MerchantService


class DungeonWindow:
    def __init__(self, root, player, dungeon_service):
        self.root = root
        self.player = player
        self.dungeon_service = dungeon_service
        self.enemy = None

        self.player.restore_combat_resources()

        self.fight_service = FightService(player, dungeon_service)
        self.merchant_service = MerchantService(player)

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

        self.event_label = tk.Label(
            self.window,
            text="",
            font=("Arial", 14)
        )
        self.event_label.pack(pady=10)

        self.status_label = tk.Label(
            self.window,
            text="",
            font=("Arial", 11),
            wraplength=450
        )
        self.status_label.pack(pady=15)

        self.buttons_frame = tk.Frame(self.window)
        self.buttons_frame.pack(pady=10)

        self.first_button = tk.Button(self.buttons_frame, width=14)
        self.first_button.pack(side="left", padx=5)

        self.second_button = tk.Button(self.buttons_frame, width=14)
        self.second_button.pack(side="left", padx=5)

        self.third_button = tk.Button(self.buttons_frame, width=14)
        self.third_button.pack(side="left", padx=5)

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
            self.event_label.config(
                text=f"{self.enemy.name}\nHP: {self.enemy.hp}"
            )

    def set_action_buttons(self, first, second, third):
        self.first_button.config(
            text=first[0],
            state="normal",
            command=first[1]
        )

        self.second_button.config(
            text=second[0],
            state="normal",
            command=second[1]
        )

        self.third_button.config(
            text=third[0],
            state="normal",
            command=third[1]
        )

    def next_room(self):
        event = self.dungeon_service.generate_event()

        if event == "combat":
            self.start_combat()
        else:
            self.show_merchant()

    def start_combat(self):
        self.enemy = self.dungeon_service.create_enemy()

        self.status_label.config(
            text=f"{self.enemy.name} appears!"
        )

        self.set_action_buttons(
            ("Attack", self.attack_enemy),
            ("Special Attack", self.special_attack),
            ("Run", self.run_away)
        )

        self.next_room_button.config(state="disabled")

        self.update_info()

    def show_merchant(self):
        self.enemy = None

        self.event_label.config(text="Merchant")
        self.status_label.config(
            text="A merchant offers you supplies."
        )

        self.set_action_buttons(
            ("Buy Heal (1)", self.buy_heal),
            ("Buy Damage (2)", self.buy_damage_bonus),
            ("Leave", self.next_room)
        )

        self.next_room_button.config(
            text="Next Room",
            state="normal",
            command=self.next_room
        )

        self.update_info()

    def buy_heal(self):
        if not self.merchant_service.buy_heal():
            self.status_label.config(text="Not enough coins.")
            return

        self.update_info()
        self.status_label.config(text="You bought healing. +30 HP.")

    def buy_damage_bonus(self):
        if not self.merchant_service.buy_damage_bonus():
            self.status_label.config(text="Not enough coins.")
            return

        self.update_info()
        self.status_label.config(text="You bought damage bonus. +5 damage.")

    def enemy_turn(self):
        enemy_damage = self.fight_service.enemy_attack(self.enemy)

        if not self.player.is_alive():
            self.update_info()
            self.status_label.config(
                text=f"{self.enemy.name} dealt {enemy_damage} damage. You were defeated!"
            )
            self.disable_action_buttons()
            self.next_room_button.config(state="disabled")
            return False

        return enemy_damage

    def attack_enemy(self):
        damage = self.fight_service.attack(self.enemy)

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
        damage = self.fight_service.special_attack(self.enemy)

        if damage is None:
            self.status_label.config(
                text="Not enough mana for special attack."
            )
            return

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
        if self.fight_service.try_escape():
            self.status_label.config(
                text="You successfully escaped from combat."
            )

            self.disable_action_buttons()
            self.next_room_button.config(state="normal")
            return

        enemy_damage = self.enemy_turn()
        self.update_info()

        if enemy_damage is not False:
            self.status_label.config(
                text=f"Escape failed! {self.enemy.name} dealt {enemy_damage} damage."
            )

    def handle_victory(self, damage):
        self.fight_service.victory(self.enemy)

        self.update_info()

        self.status_label.config(
            text=(
                f"You dealt {damage} damage. "
                f"You defeated {self.enemy.name}! "
                f"+{self.enemy.coin_reward} coin."
            )
        )

        self.disable_action_buttons()
        self.next_room_button.config(state="normal")

    def disable_action_buttons(self):
        self.first_button.config(state="disabled")
        self.second_button.config(state="disabled")
        self.third_button.config(state="disabled")