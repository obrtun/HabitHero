import tkinter as tk


class DungeonWindow:
    def __init__(self, root, player, dungeon_service):
        self.root = root
        self.player = player
        self.dungeon_service = dungeon_service
        self.enemy = self.dungeon_service.create_enemy()

        self.player.restore_hp()

        self.window = tk.Toplevel(self.root)
        self.window.title("Dungeon")
        self.window.geometry("400x350")
        self.window.resizable(False, False)

        self.create_widgets()
        self.update_info()

    def create_widgets(self):
        self.title_label = tk.Label(
            self.window,
            text="Dungeon",
            font=("Arial", 20, "bold")
        )
        self.title_label.pack(pady=10)

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

        self.attack_button = tk.Button(
            self.window,
            text="Attack",
            font=("Arial", 12),
            command=self.attack_enemy
        )
        self.attack_button.pack(pady=10)

        self.status_label = tk.Label(
            self.window,
            text="A wild enemy appears!",
            font=("Arial", 11),
            wraplength=350
        )
        self.status_label.pack(pady=10)

    def update_info(self):
        self.player_label.config(
            text=f"Player HP: {self.player.current_hp}/{self.player.max_hp}"
        )

        self.enemy_label.config(
            text=f"{self.enemy.name}\nHP: {self.enemy.hp}"
        )

    def attack_enemy(self):
        player_damage = self.dungeon_service.calculate_player_damage(
            self.player
        )

        self.enemy.take_damage(player_damage)

        if not self.enemy.is_alive():
            self.update_info()
            self.status_label.config(
                text=f"You dealt {player_damage} damage. You defeated {self.enemy.name}!"
            )
            self.attack_button.config(state="disabled")
            return

        enemy_damage = self.dungeon_service.calculate_enemy_damage(
            self.player,
            self.enemy
        )

        self.player.take_damage(enemy_damage)

        self.update_info()

        if not self.player.is_alive():
            self.status_label.config(
                text=f"You dealt {player_damage} damage. {self.enemy.name} defeated you!"
            )
            self.attack_button.config(state="disabled")
            return

        self.status_label.config(
            text=f"You dealt {player_damage} damage. {self.enemy.name} dealt {enemy_damage} damage."
        )