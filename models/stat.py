class Stat:
    def __init__(self, name):
        self.name = name
        self.value = 10
        self.progress = 0

    def add_progress(self, amount):
        self.progress += amount

        while self.progress >= 100:
            self.progress -= 100
            self.value += 1

    def to_dict(self):
        return {
            "name": self.name,
            "value": self.value,
            "progress": self.progress
        }

    @classmethod
    def from_dict(cls, data):
        stat = cls(data["name"])

        stat.value = data["value"]
        stat.progress = data["progress"]

        return stat