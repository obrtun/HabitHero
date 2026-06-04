class HabitService:
    def __init__(self):
        self.habits = []

    def add_habit(self, habit):
        self.habits.append(habit)

    def get_habits(self):
        return self.habits

    def remove_habit(self, habit_name):
        self.habits = [
            habit for habit in self.habits
            if habit.name != habit_name
        ]

    def complete_habit(self, player, habit):
        stat = player.get_stat(habit.stat_key)
        stat.add_progress(habit.reward)