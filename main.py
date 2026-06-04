from models.player import Player
from models.habit import Habit
from services.habit_service import HabitService


player = Player("Hero")
habit = Habit("Gym", "physique", 25)

habit_service = HabitService()
habit_service.complete_habit(player, habit)

physique = player.get_stat("physique")

print(physique.value)
print(physique.progress)