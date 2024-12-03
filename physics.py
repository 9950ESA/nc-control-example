# FILE: physics.py

import time

class PhysicsSimulation:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.target_x = x
        self.target_y = y
        self.target_z = z

    def move_to(self, new_x, new_y, new_z):
        self.target_x = new_x
        self.target_y = new_y
        self.target_z = new_z

    def update(self):
        if self.x < self.target_x:
            self.x += 1
        elif self.x > self.target_x:
            self.x -= 1
        if self.y < self.target_y:
            self.y += 1
        elif self.y > self.target_y:
            self.y -= 1
        if self.z < self.target_z:
            self.z += 1
        elif self.z > self.target_z:
            self.z -= 1
        print(f"Current position {self.x}, {self.y}, {self.z}")
        time.sleep(0.05)
# Example usage:
if __name__ == "__main__":
    sim = PhysicsSimulation()
    sim.move_to(100, 100, 100)
    sim.move_to(200, 100, 100)