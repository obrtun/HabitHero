import tkinter as tk
from tkinter import ttk

from services.dungeon_service import DungeonService
from views.dungeon_window import DungeonWindow
from views.add_habit_window import AddHabitWindow


class MainWindow:
    def __init__(self, player, habit_service, save_service):
        self.player = player
        self.habit_service = habit_service
        self.save_service = save_service

        self.root = tk.Tk()
        self.root.title("Habit RPG")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        self.header_frame = tk.Frame(self.root)
        self.header_frame.pack(fill="x", pady=10)

        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill="both", expand=True)

        self.habits_frame = tk.Frame(self.content_frame)
        self.habits_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        self.stats_frame = tk.Frame(self.content_frame)
        self.stats_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(fill="x", pady=10)

        tk.Label(
            self.header_frame,
            text="Habit RPG",
            font=("Arial", 24, "bold")
        ).pack()

        tk.Label(
            self.habits_frame,
            text="Habits",
            font=("Arial", 16, "bold")
        ).pack(anchor="w")

        tk.Label(
            self.stats_frame,
            text="Stats",
            font=("Arial", 16, "bold")
        ).pack(anchor="w")

        self.create_habits_panel()
        self.create_stats_panel()

        self.dungeon_button = tk.Button(
            self.bottom_frame,
            text="Enter Dungeon",
            command=self.open_dungeon_window
        )

        self.dungeon_button.pack()

        self.status_label = tk.Label(
            self.bottom_frame,
            text="Welcome to Habit RPG!",
            font=("Arial", 11)
        )
        self.status_label.pack(pady=5)

    def open_dungeon_window(self):
        dungeon_service = DungeonService()
        DungeonWindow(self.root, self.player, dungeon_service)

    def create_stats_panel(self):
        self.stat_labels = {}
        self.stat_progress_bars = {}

        for stat_key, stat in self.player.stats.items():
            stat_frame = tk.Frame(self.stats_frame)
            stat_frame.pack(anchor="w", fill="x", pady=8)

            label = tk.Label(
                stat_frame,
                text=f"{stat.name}: {stat.value} ({stat.progress}/100)",
                font=("Arial", 12)
            )
            label.pack(anchor="w")

            progress_bar = ttk.Progressbar(
                stat_frame,
                maximum=100,
                value=stat.progress,
                length=250
            )
            progress_bar.pack(anchor="w", pady=3)

            self.stat_labels[stat_key] = label
            self.stat_progress_bars[stat_key] = progress_bar

    def create_habits_panel(self):
        self.habits_container = tk.Frame(self.habits_frame)
        self.habits_container.pack(fill="both", expand=True, pady=10)

        self.habits_canvas = tk.Canvas(self.habits_container)
        self.habits_canvas.pack(side="left", fill="both", expand=True)

        self.habits_scrollbar = tk.Scrollbar(
            self.habits_container,
            orient="vertical",
            command=self.habits_canvas.yview
        )
        self.habits_scrollbar.pack(side="right", fill="y")

        self.habits_canvas.configure(
            yscrollcommand=self.habits_scrollbar.set
        )

        self.habits_list_frame = tk.Frame(self.habits_canvas)

        self.habits_canvas.create_window(
            (0, 0),
            window=self.habits_list_frame,
            anchor="nw"
        )

        self.habits_list_frame.bind(
            "<Configure>",
            lambda event: self.habits_canvas.configure(
                scrollregion=self.habits_canvas.bbox("all")
            )
        )

        self.add_habit_button = tk.Button(
            self.habits_frame,
            text="+ Add Habit",
            font=("Arial", 12),
            command=self.open_add_habit_window
        )
        self.add_habit_button.pack(pady=5)

        self.update_habit_list()

    def update_stats(self):
        for stat_key, stat in self.player.stats.items():
            self.stat_labels[stat_key].config(
                text=f"{stat.name}: {stat.value} ({stat.progress}/100)"
            )

            self.stat_progress_bars[stat_key]["value"] = stat.progress

    def update_habit_list(self):
        for widget in self.habits_list_frame.winfo_children():
            widget.destroy()

        for habit in self.habit_service.get_sorted_habits():
            habit_row = tk.Frame(self.habits_list_frame)
            habit_row.pack(fill="x", pady=5)

            habit_label = tk.Label(
                habit_row,
                text=f"{habit.name} → +{habit.reward} {habit.stat_key}",
                font=("Arial", 12),
                anchor="w",
                width=28
            )
            habit_label.pack(side="left")

            complete_button = tk.Button(
                habit_row,
                text="Completed" if self.habit_service.is_completed_today(habit) else "Complete",
                state="disabled" if self.habit_service.is_completed_today(habit) else "normal",
                command=lambda h=habit: self.complete_habit(h)
            )
            complete_button.pack(side="left", padx=5)

            delete_button = tk.Button(
                habit_row,
                text="Delete",
                command=lambda h=habit: self.delete_habit(h)
            )
            delete_button.pack(side="left")

    def save_data(self):
        self.save_service.save(
            self.player,
            self.habit_service.get_habits()
        )

    def complete_habit(self, habit):
        self.habit_service.complete_habit(self.player, habit)

        self.save_data()
        self.update_stats()
        self.update_habit_list()

        self.status_label.config(
            text=f"{habit.name} completed! +{habit.reward} {habit.stat_key}"
        )

    def delete_habit(self, habit):
        self.habit_service.remove_habit(habit.name)

        self.save_data()
        self.update_habit_list()

        self.status_label.config(
            text=f"Habit '{habit.name}' deleted."
        )

    def open_add_habit_window(self):
        AddHabitWindow(
            self.root,
            self.player,
            self.habit_service,
            self.save_service,
            self.on_habit_created
        )

    def on_habit_created(self, message):
        self.update_habit_list()

        self.status_label.config(
            text=message
        )

    def run(self):
        self.root.mainloop()