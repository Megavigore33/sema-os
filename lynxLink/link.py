##################################################
###  Code fait par Tristan Radaelli--Quillacq  ###
###  Client SemaLynx                           ###
###  version : 0.2 - 29/01/2023                ###
##################################################

import socket
import select
import errno
import subprocess
from threading import Thread
from scan import scan, create_result


HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 5001

my_username = "clientTest1"

netscanResult = ""

# Fonction exécutant un reboot
def rebootAsked():
    subprocess.run(["reboot"], shell=True)
    
# Fonction exécutant le script de ping
def pingAsked():
    subprocess.run(["python3 ping.py"], shell=True)

def netscanAsked(ip, portsList):
    result = scan(ip, portsList) # Fait le netscan avec les infos récupérées
    # netscanData = create_result(result)
    create_result(result)
    
def debitAsked():
    subprocess.run(["python3 debit.py"], shell=True)

def updateAsked():
    subprocess.run(["python3 .../SemaOS-Updater/updater.py"], shell=True)

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
                    # Si il nous est adressé, exécuter le ping
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
                    t3 = Thread(target=debitAsked) # Attribue un thread pour l'exécution du test de débit
                    t3.start() # Exécute le test de débit
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
                    # Si il nous est adressé, exécuter le netscan
                    portsString = messageSplit[3].split(",") # Récupération des ports saisis
                    portsInt = []
                    for i in portsString:
                        portsInt.append(int(i))
                    ipaddr = messageSplit[2] # Récupération de l'IP saisie
                    t2 = Thread(target=netscanAsked(ipaddr, portsInt)) # Attribue un thread pour l'exécution du netscan
                    t2.start() # Exécute le netscan
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
            elif "/viewdebit" in message:
                # Si viewdebit, vérifié qu'il nous est adressé
                messageSplit = message.split()
                viewdebitRequester = messageSplit[1]
                if viewdebitRequester == my_username:
                    # Transmet les logs du dernier test de debit effectué
                    pingfile = open("./debit.txt", "r")
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
            elif "/viewnetscan" in message:
                # Si netscan, vérifié qu'il nous est adressé
                messageSplit = message.split()
                netscanRequester = messageSplit[1]
                if netscanRequester == my_username:
                    # Transmet les logs du dernier netscan effectué
                    nscanfile = open("./netscan.txt", "r")
                    data = nscanfile.read()
                    message = data.encode('utf-8')
                    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(message_header + message)
                else:
                    # Paquet pour un autre client
                    data = "nok"
                    message = data.encode('utf-8')
                    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(message_header + message)
            elif "/update" in message:
                messageSplit = message.split()
                updateRequester = messageSplit[1]
                if updateRequester == my_username:
                    data = "update ok!"
                    message = data.encode('utf-8')
                    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(message_header + message)
                    updateAsked() # Exécute le reboot
                else:
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