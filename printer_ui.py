import pygame

PADDING = 20

class rectangle: # simple rectangle
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
class grey_red_rectangle: # grey rectangle with movable small red rectangle on top
    color_grey = (100, 100, 100)
    color_red = (255, 0, 0)
    red_size = 10

    def __init__(self, x, y, width, height):
        self.grey = rectangle(x, y, width, height, self.color_grey)
        self.red = rectangle(0, 0, self.red_size, self.red_size, self.color_red)

    def move_to(self, x_fraction, y_fraction):
        self.red.x = self.grey.x + x_fraction * (self.grey.width - self.red_size)
        self.red.y = self.grey.y + y_fraction * (self.grey.height - self.red_size)

    def draw(self, screen):
        self.grey.draw(screen)
        self.red.draw(screen)

class printer_ui: # two rectangles, one for top view, one for side view drawn side to side
    def __init__(self):
        self.top_view = grey_red_rectangle(PADDING, PADDING, 150, 200)
        self.side_view = grey_red_rectangle(PADDING + self.top_view.grey.width + PADDING, 100, 150, 120)

    def move_to(self, x, y, z):
        self.top_view.move_to(x, y)
        self.side_view.move_to(x, z)

    def draw(self, screen):
        self.top_view.draw(screen)
        self.side_view.draw(screen)