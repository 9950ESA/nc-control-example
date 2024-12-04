import pygame
import threading
import queue
import time
import socket
from physics import PhysicsSimulation
from printer_ui import printer_ui

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PRINTER_START = (400, 300)

#ender 3 v2 mitat 220 x 220 x 250 mm
PRINTER_AREA = (220, 220, 250)


physics_to_ui = queue.Queue()  
socket_to_physics = queue.Queue() 
physics_to_socket = queue.Queue()  

def ui_thread():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Moving Box Animation")
    printer_view = printer_ui()

    #valmistellaan näyttämö
    screen.fill((0,0,0))
    printer_view.move_to(0, 0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
        try:
            command = physics_to_ui.get_nowait()
            x, y, z = command
            a, b, c = PRINTER_AREA
            xx, yy, zz = x/a, y/b, z/c

            #piilotetaan vanhat merkit
            screen.fill((0,0,0))

            printer_view.move_to(xx, yy, zz)
        except:
            pass

        printer_view.draw(screen)
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    pygame.quit()


def physics_thread():
    sim = PhysicsSimulation()
    while True:
        try:
            command = socket_to_physics.get_nowait()

            if command["action"] == "move":
                print("siirtokomento")
                x, y, z = command["target"]

                #tehdään väliliikkeet
                while(sim.move_to(x, y, z)):
                    physics_to_socket.put((sim.x, sim.y, sim.z))
                    physics_to_ui.put((sim.x, sim.y, sim.z))
                    time.sleep(0.05) #estetään tukkeutuminen
                
                #perillä olevat koordinaatit
                physics_to_socket.put((sim.x, sim.y, sim.z))
                physics_to_ui.put((sim.x, sim.y, sim.z))

        except queue.Empty:
            pass

def socket_thread():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12345))
    server_socket.listen(5)
    coords = (0, 0, 0)
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

                while True: #tyhjätään jono
                    try:
                        coords = physics_to_socket.get_nowait()
                    except queue.Empty:
                        break

                x, y, z = coords 
                response = f"POSITION {x} {y} {z}"
                client_socket.sendall(response.encode())
                print(f"Lähetettiin koordinaatit {response}")
        
ui = threading.Thread(target=ui_thread)
physics = threading.Thread(target=physics_thread)
socket_comm = threading.Thread(target=socket_thread, daemon=True)

ui.start()
physics.start()
socket_comm.start()

ui.join()

