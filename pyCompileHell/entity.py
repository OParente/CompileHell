class Entity:
    def __init__(self, name):
        self.name = name
        self.x = 0
        self.y = 0

    def draw(self):
        # in a real engine you'd call the native draw
        print(f"Entity {self.name} draw at ({self.x},{self.y})")
