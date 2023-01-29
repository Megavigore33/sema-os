##################################################
###  Code fait par Tristan Radaelli--Quillacq  ###
###  Client SemaLynx                           ###
###  version : 0.1 - 29/01/2023                ###
##################################################

import socket
import select
import errno
import subprocess
from threading import Thread

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 5001

my_username = "clientTest1"

# Fonction exécutant un reboot
def rebootAsked():
    subprocess.run(["reboot"], shell=True)
    
# Fonction exécutant le script de ping
def pingAsked():
    subprocess.run(["python3 ping.py"], shell=True)

# Créé un client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connexion du socket au serveur
client_socket.connect((IP, PORT))

# Autorise la réception des paquets
client_socket.setblocking(False)

# Prépare un paquet contenant le nom du client et l'envoi au serveur
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True:
    #message = input(f'{my_username} > ')

    try:
        # Boucle infinie en attente de requête du serveur
        while True:

            # Stoque le header du paquet
            username_header = client_socket.recv(HEADER_LENGTH)

            # Vérifie que le header est correct, si non serveur ko
            if not len(username_header):
                print('Connection closed by the server')
                #sys.exit()

            # Converti le header en int
            username_length = int(username_header.decode('utf-8').strip())

            # Decode le nom du serveur
            username = client_socket.recv(username_length).decode('utf-8')

            # # Decode le message du serveur
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            # Affiche la requête du serveur
            print(f'{username} > {message}')
            
            # Traitement de la requête du serveur
            if "/reboot" in message:
                # Si reboot, vérifié qu'il nous est adressé
                messageSplit = message.split()
                shutdownRequester = messageSplit[1]
                if shutdownRequester == my_username:
                    # Si il nous est adressé, exécuter le reboot
                    data = "reboot ok!"
                    message = data.encode('utf-8')
                    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(message_header + message)
                    rebootAsked() # Exécute le reboot
                else:
                    # Paquet pour un autre client
                    data = "nok"
                    message = data.encode('utf-8')
                    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(message_header + message)
            elif "/ping" in message:
                # Si ping, vérifié qu'il nous est adressé
                messageSplit = message.split()
                pingRequester = messageSplit[1]
                if pingRequester == my_username:
                    t1 = Thread(target=pingAsked) # Attribue un thread pour l'exécution du ping
                    t1.start() # Exécute le ping
                    
                    data = "ping ok!"
                    message = data.encode('utf-8')
                    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(message_header + message)
                else:
                    # Paquet pour un autre client
                    data = "nok"
                    message = data.encode('utf-8')
                    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(message_header + message)
            elif "/debit" in message:
                # Si debit, vérifié qu'il nous est adressé
                messageSplit = message.split()
                debitRequester = messageSplit[1]
                if debitRequester == my_username:
                    # Si il nous est adressé, exécuter le test de débit
                    subprocess.run(["python3 ../scripts/testdebit.py"], shell=True)
                    data = "debit ok!"
                    message = data.encode('utf-8')
                    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(message_header + message)
                else:
                    # Paquet pour un autre client
                    data = "nok"
                    message = data.encode('utf-8')
                    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(message_header + message)
            elif "/netscan" in message:
                # Si netscan, vérifié qu'il nous est adressé
                messageSplit = message.split()
                netscanRequester = messageSplit[1]
                if netscanRequester == my_username:
                    # Si il nous est adressé, exécuter le netscan (pas fait)
                    data = "netscan ok!"
                    message = data.encode('utf-8')
                    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(message_header + message)
                else:
                    # Paquet pour un autre client
                    data = "nok"
                    message = data.encode('utf-8')
                    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(message_header + message)
            elif "/viewping" in message:
                # Si viewping, vérifié qu'il nous est adressé
                messageSplit = message.split()
                viewpingRequester = messageSplit[1]
                if viewpingRequester == my_username:
                    # Transmet les logs du dernier ping effectué
                    pingfile = open("./ping.txt", "r")
                    data = pingfile.read()
                    message = data.encode('utf-8')
                    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(message_header + message)
                else:
                    # Paquet pour un autre client
                    data = "nok"
                    message = data.encode('utf-8')
                    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(message_header + message)
            
    # Gestion d'exception de lecture du paquet
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Erreur lecture : {}'.format(str(e)))

        continue

    # Gestion d'exception autre
    except Exception as e:
        print('Erreur : '.format(str(e)))