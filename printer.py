import pygame
import threading
import queue
import time
import socket

# Constants for the screen and printer
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PRINTER_START = (400, 300)

# Shared queues
ui_to_physics = queue.Queue()  # Commands for the physics thread
physics_to_ui = queue.Queue()  # Updates for the UI
socket_to_physics = queue.Queue()  # Commands from the socket thread

def ui_thread():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Printer Animation")
    clock = pygame.time.Clock()
    printer_position = PRINTER_START

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check for updates from physics
        try:
            printer_position = physics_to_ui.get_nowait()
        except queue.Empty:
            pass

        # Clear screen and draw printer
        screen.fill((30, 30, 30))
        pygame.draw.circle(screen, (0, 255, 0), printer_position, 10)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

def physics_thread():
    position = list(PRINTER_START)
    target = list(PRINTER_START)

    while True:
        try:
            # Handle new commands from UI
            command = ui_to_physics.get_nowait()
            if command["action"] == "move":
                target = command["target"]
        except queue.Empty:
            pass

        try:
            # Handle new commands from socket
            command = socket_to_physics.get_nowait()
            if command["action"] == "move":
                target = command["target"]
        except queue.Empty:
            pass

        # Simple physics: move towards the target
        if position != target:
            for i in range(2):
                if position[i] < target[i]:
                    position[i] += 1
                elif position[i] > target[i]:
                    position[i] -= 1

                # Ensure the position stays within the screen boundaries
                position[i] = max(0, min(position[i], SCREEN_WIDTH if i == 0 else SCREEN_HEIGHT))

            # Send updates to the UI thread
            physics_to_ui.put(tuple(position))

        time.sleep(0.01)

def socket_thread():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12345))
    server_socket.listen(5)

    while True:
        client_socket, _ = server_socket.accept()
        with client_socket:
            data = client_socket.recv(1024).decode()
            if data.startswith("MOVE"):
                _, x, y = data.split()
                socket_to_physics.put({"action": "move", "target": (int(x), int(y))})

# Start the threads
ui = threading.Thread(target=ui_thread)
physics = threading.Thread(target=physics_thread)
socket_comm = threading.Thread(target=socket_thread, daemon=True)

ui.start()
physics.start()
socket_comm.start()

ui.join()