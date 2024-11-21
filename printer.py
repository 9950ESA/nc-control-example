import pygame
import sys

from printer_ui import printer_ui

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving Box Animation")

printer_view = printer_ui()
x = 0
y = 0
z = 0
go_right = True

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black
    screen.fill((0,0,0))    

    if x > 1:
        go_right = False
    elif x < 0:
        go_right = True

    if go_right:
        x += 0.01
        y += 0.01
        z += 0.01
    else:
        x -= 0.01
        y -= 0.01
        z -= 0.01
    printer_view.move_to(x, y, z)

    # Draw the box
    printer_view.draw(screen)

    # Update the display
    pygame.display.flip()
    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
