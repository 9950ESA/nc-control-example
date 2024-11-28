import time

class PhysicsSimulation:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def move_to(self, new_x, new_y, new_z):
        while True:
            if self.x < new_x:
                self.x += 1
            elif self.x > new_x:
                self.x -= 1
            if self.y < new_y:
                self.y += 1
            elif self.y > new_y:
                self.y -= 1
            if self.z < new_z:
                self.z += 1
            elif self.z > new_z:
                self.z -= 1
            if self.x == new_x and self.y == new_y and self.z == new_z:
                break
            print(f"Current position {self.x}, {self.y}, {self.z}")
            time.sleep(0.05)        

# Example usage:
if __name__ == "__main__":
    sim = PhysicsSimulation()
    sim.move_to(100, 100, 100)
    sim.move_to(200, 100, 100)