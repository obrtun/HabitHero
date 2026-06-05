from models.player import Player
from services.habit_service import HabitService
from services.save_service import SaveService
from views.main_window import MainWindow


save_service = SaveService()

loaded_data = save_service.load()

if loaded_data:
    player, habits = loaded_data
else:
    player = Player("Hero")
    habits = []

habit_service = HabitService()

for habit in habits:
    habit_service.add_habit(habit)

window = MainWindow(player, habit_service, save_service)
window.run()

