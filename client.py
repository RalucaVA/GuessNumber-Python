import socket
import sys

def send_guess():
    guess = input()
    print("Ai introdus numarul: {}".format(guess))
    client_socket.send(guess.encode())
    message = client_socket.recv(1024).decode().strip()
    print(message)
    if "Felicitări! Ai ghicit corect!" in message:
        return True
    return False


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
try:
    port = 12345
    if port != 12345:
        print("Serverul asculta pe portul 12345. Schimba portul '{}' cu 12345".format(port))
        sys.exit()
    client_socket.connect((host, port))

    while True:
        message = client_socket.recv(1024).decode().strip()
        print(message)
        if "Bine ai venit! Asteapta să iti vina randul sa ghicesti." in message:
            continue
        if "Celalalt client a ghicit corect." in message:
            break
        correct = send_guess()
        if correct: 
            break

except socket.error:
    print("Serverul nu este pornit")
finally:
    client_socket.close()
