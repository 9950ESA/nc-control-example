import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving Box Animation")

# Define colors
black = (0, 0, 0)
red = (255, 0, 0)

# Box properties
box_size = 50
box_x = 0
box_y = (height - box_size) // 2
box_speed = 5

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the box
    box_x += box_speed
    if box_x > width:
        box_x = -box_size

    # Fill the screen with black
    screen.fill(black)

    # Draw the box
    pygame.draw.rect(screen, red, (box_x, box_y, box_size, box_size))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
