import pygame
import sys

class rectangle:
    x = 0
    y = 0
    width = 100
    height = 100
    color = (255, 0, 0)

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move_on(self, rect, x_fraction, y_fraction):
        self.x = rect.x + x_fraction * rect.width
        self.y = rect.y + y_fraction * rect.height

    def get_fraction(self, rect):
        return (self.x - rect.x) / rect.width, (self.y - rect.y) / rect.height


# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving Box Animation")

PADDING = 20

plate_top = rectangle(PADDING, PADDING, 150, 200, (100, 100, 100))
print_head_top = rectangle(40, 40, 10, 10, (255, 0, 0))
plate_side = rectangle(PADDING + plate_top.width + PADDING, 100, 150, 120, (100, 100, 100))
print_head_side = rectangle(300, 50, 10, 10, (255, 0, 0))

print_head_top.move_on(plate_top, 0, 0)
print_head_side.move_on(plate_side, 0, 0)

x = 0
y = 0
go_right = True

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black
    screen.fill((0,0,0))

    print_head_top.move_on(plate_top, x, y)
    print_head_side.move_on(plate_side, x, y)

    if x > 1:
        go_right = False
    elif x < 0:
        go_right = True

    if go_right:
        x += 0.01
        y += 0.01
    else:
        x -= 0.01
        y -= 0.01

    # Draw the box
    plate_top.draw(screen)
    print_head_top.draw(screen)
    plate_side.draw(screen)
    print_head_side.draw(screen)

    # Update the display
    pygame.display.flip()
    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
