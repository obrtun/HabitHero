import tkinter as tk
from tkinter import messagebox

from models.habit import Habit

from exceptions.habit_exceptions import InvalidHabitNameError
from utils.validators import validate_habit_name


class AddHabitWindow:

    DIFFICULTY_REWARDS = {
        "Easy": 10,
        "Medium": 20,
        "Hard": 35
    }

    def __init__(
        self,
        parent,
        player,
        habit_service,
        save_service,
        on_habit_created
    ):
        self.player = player
        self.habit_service = habit_service
        self.save_service = save_service
        self.on_habit_created = on_habit_created

        self.window = tk.Toplevel(parent)
        self.window.title("Add Habit")
        self.window.geometry("300x260")
        self.window.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.window, text="Habit name:").pack(pady=5)

        self.name_entry = tk.Entry(self.window)
        self.name_entry.pack(pady=5)

        tk.Label(self.window, text="Stat:").pack(pady=5)

        self.stat_var = tk.StringVar(value="physique")

        tk.OptionMenu(
            self.window,
            self.stat_var,
            "physique",
            "education",
            "sociality",
            "discipline",
            "creativity"
        ).pack(pady=5)

        tk.Label(self.window, text="Difficulty:").pack(pady=5)

        self.difficulty_var = tk.StringVar(value="Medium")

        tk.OptionMenu(
            self.window,
            self.difficulty_var,
            "Easy",
            "Medium",
            "Hard"
        ).pack(pady=5)

        tk.Button(
            self.window,
            text="Create",
            command=self.create_habit
        ).pack(pady=15)

    def create_habit(self):
        name = self.name_entry.get().strip()
        stat_key = self.stat_var.get()
        difficulty = self.difficulty_var.get()

        try:
            validate_habit_name(name)

        except InvalidHabitNameError as error:
            messagebox.showwarning(
                "Invalid habit name",
                str(error)
            )
            return

        reward = self.DIFFICULTY_REWARDS[difficulty]

        habit = Habit(
            name,
            stat_key,
            reward
        )

        self.habit_service.add_habit(habit)

        self.save_service.save(
            self.player,
            self.habit_service.habits
        )

        self.on_habit_created(
            f"Habit '{name}' created! Difficulty: {difficulty}"
        )

        self.window.destroy()