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

def ui_thread():
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


def physics_thread():
    # Check for updates from physics
    try:
        printer_target_position = socket_to_physics.get_nowait()
    except queue.Empty:
        pass
    x = 0
    y = 0
    z = 0
    

def socket_thread():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12345))
    server_socket.listen(5)

    while True:
        client_socket, _ = server_socket.accept()
        with client_socket:
            data = client_socket.recv(1024).decode()
            if data.startswith("MOVE"):
                _, x, y, z = data.split()
                socket_to_physics.put({"action": "move", "target": (int(x), int(y), int(z))})

# Start the threads
ui = threading.Thread(target=ui_thread)
physics = threading.Thread(target=physics_thread)
socket_comm = threading.Thread(target=socket_thread, daemon=True)

ui.start()
physics.start()
socket_comm.start()

ui.join()