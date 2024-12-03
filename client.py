import socket

def send_move_command(x, y, z):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 12345))
        command = f"MOVE {x} {y} {z}"
        s.sendall(command.encode())
        response = s.recv(1024).decode()
        print("Received:", response)

def get_position():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 12345))
        command = "GET_POSITION"
        s.sendall(command.encode())
        response = s.recv(1024).decode()
        print("Received:", response)

if __name__ == "__main__":
    while True:
        try:
            action = input("Enter 'move' to send MOVE command or 'get' to get current position: ").strip().lower()
            if action == "move":
                x = float(input("Enter x coordinate: "))
                y = float(input("Enter y coordinate: "))
                z = float(input("Enter z coordinate: "))
                send_move_command(x, y, z)
            elif action == "get":
                get_position()
            else:
                print("Invalid action. Please enter 'move' or 'get'.")
        except ValueError:
            print("Please enter valid numbers.")
        except KeyboardInterrupt:
            print("\nClient exiting.")
            break