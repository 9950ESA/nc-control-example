import pygame
import threading
import queue
import time
import socket
from physics import PhysicsSimulation
from printer_ui import printer_ui

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PRINTER_START = (400, 300)

physics_to_ui = queue.Queue()  
socket_to_physics = queue.Queue() 
physics_to_scocket = queue.Queue()  

def ui_thread():
    from printer_ui import printer_ui
    # Initialize Pygame
    pygame.init()
    # Set up the display
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Moving Box Animation")
    printer_view = printer_ui()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Fill the screen with black
        screen.fill((0, 0, 0))
        
        # Check for updates from physics
        try:
            x, y, z = physics_to_ui.get_nowait()
            printer_view.move_to(x, y, z)
        except queue.Empty:
            pass
        
        # Draw the updated view
        printer_view.draw(screen)
        
        # Update the display
        pygame.display.flip()
        
        # Cap the frame rate
        pygame.time.Clock().tick(60)
    
    pygame.quit()


def physics_thread():
    sim = PhysicsSimulation()
    while True:
        try:
            command = socket_to_physics.get_nowait()

            if command["action"] == "move":
                x, y, z = command["target"]
                sim.move_to(x, y, z)

            if command["action"] == "getpos":
                physics_to_scocket.put((sim.x, sim.y, sim.z))

        except queue.Empty:
            pass
        sim.update()
        physics_to_ui.put((sim.x, sim.y, sim.z))

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
                socket_to_physics.put({"action": "move", "target": (float(x), float(y), float(z))})
                response = "OK"
                client_socket.sendall(response.encode())

            elif data == "GET_POSITION":
                try:
                    socket_to_physics.put({"action": "getpos"})
                    x, y, z = physics_to_scocket.get_nowait()
                    response = f"POSITION {x} {y} {z}"
                    print(response)
                    client_socket.sendall(response.encode())
                except queue.Empty:
                    response = "POSITION not available"
                    client_socket.sendall(response.encode())
        
ui = threading.Thread(target=ui_thread)
physics = threading.Thread(target=physics_thread)
socket_comm = threading.Thread(target=socket_thread, daemon=True)

ui.start()
physics.start()
socket_comm.start()

ui.join()