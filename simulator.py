import pygame
import threading
import queue
import time
import socket

# Constants for the screen and printer
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PRINTER_START = (400, 300)

# Shared queues
physics_to_ui = queue.Queue()  # Updates for the UI
socket_to_physics = queue.Queue()  # Commands from the socket thread
physics_to_scocket = queue.Queue()  # Commands for the physics thread

def send_move_command(x, y):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 12345))
        s.sendall(f"MOVE {x} {y}".encode())

def ui_thread():
    from printer_ui import printer_ui
    # Initialize Pygame
    pygame.init()
    # Set up the display
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Control the Printer")
    printer_view = printer_ui()
    x = 400
    y = 300
    z = 0
    go_right = True

    # Initialize font
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 25)

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    x = min(x + 10, width)
                elif event.key == pygame.K_LEFT:
                    x = max(x - 10, 0)
                elif event.key == pygame.K_UP:
                    y = max(y - 10, 0)
                elif event.key == pygame.K_DOWN:
                    y = min(y + 10, height)
                send_move_command(x, y)

        # Clear the screen
        screen.fill((0, 0, 0))

        # Render the text
        text_surface = font.render(f'X: {x}, Y: {y}', True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

        # Handle other UI updates here

        # Update the display
        pygame.display.flip()

    pygame.quit()

# Start the UI thread
ui = threading.Thread(target=ui_thread)
ui.start()
ui.join()