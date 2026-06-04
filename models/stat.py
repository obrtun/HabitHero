class Stat:
    def __init__(self, name, value = 10, progress = 0):
        self.name = name
        self.value = value
        self.progress = progress

    def add_progress(self, amount):
        self.progress += amount

        while self.progress >= 100:
            self.progress -= 100
            self.value += 1