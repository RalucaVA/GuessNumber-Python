import socket
import random

MIN_NUMBER = 1
MAX_NUMBER = 100


number_to_guess = random.randint(MIN_NUMBER, MAX_NUMBER)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


host = socket.gethostname()
port = 12345

server_socket.bind((host, port))

server_socket.listen(2)

print("Serverul este activ și ascultă conexiuni...")
client1_socket, client1_address = server_socket.accept()
print("Clientul 1 conectat:", client1_address)
client1_socket.send("Bine ai venit! Ghiceste un număr intre {} și {}:".format(MIN_NUMBER, MAX_NUMBER).encode())


client2_socket, client2_address = server_socket.accept()
print("Clientul 2 conectat:", client2_address)
client2_socket.send("Bine ai venit! Asteapta să iti vina randul sa ghicesti.".encode())


def check_guess(guess):
    try:
        print("Se compara numarul primit cu {}".format(number_to_guess))
        guess = int(guess)
        if guess < MIN_NUMBER or guess > MAX_NUMBER:
            return "Numărul trebuie să fie între {} și {}.".format(MIN_NUMBER, MAX_NUMBER), False
        elif guess == number_to_guess:
            return "Felicitări! Ai ghicit corect!", True
        elif guess < number_to_guess:
            return "Numărul este prea mic. Asteapta-ti randul.", False
        else:
            return "Numărul este prea mare. Asteapta-ti randul.", False
    except ValueError:
        return "Te rog introdu un număr întreg.", False


while True:
        guess = client1_socket.recv(1024).decode().strip()
        print(guess)
        message, correct = check_guess(guess)
        client1_socket.send(message.encode())
        if correct:        
            print("Clientul 1 a ghicit corect.")
            client2_socket.send("Celalalt client a ghicit corect.".encode())
            break
        client2_socket.send("Este rândul tău să ghicești. Introdu un număr între {} și {}".format(MIN_NUMBER, MAX_NUMBER).encode())
        guess = client2_socket.recv(1024).decode().strip()
        print(guess)
        message, correct = check_guess(guess)
        client2_socket.send(message.encode())
        if correct:        
            print("Clientul 2 a ghicit corect.")
            client1_socket.send("Celalalt client a ghicit corect.".encode())
            break
        client1_socket.send("Este rândul tău să ghicești. Introdu un număr între {} și {}".format(MIN_NUMBER, MAX_NUMBER).encode())


client1_socket.close()
client2_socket.close()
server_socket.close()

