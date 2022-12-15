import socket
from server_setup import *
from _thread import *
import sys

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Constantes
BUFFER_SIZE = 2048  # Tamaño del buffer
HOST = socket.gethostname()  # Obtiene el nombre de la máquina
SERVER_IP = socket.gethostbyname(HOST)  # Obtiene la IP de la máquina
PORT = 8888  # Puerto de conexión

# Conexión
try:
    socket_server.bind((SERVER_IP, PORT))
except socket.error as e:
    print(str(e))

socket_server.listen(2)  # Escucha a 2 clientes
print(f"Esperando conexión, servidor iniciado en {HOST} con IP {SERVER_IP}")

# Variables globales
current_id = 1


def threaded_client(conn):
    global current_id
    id_client = current_id
    current_id += 1
    config_client = f"{id_client}:{FREE_COORDINATES}:{WALL_COORDINATES}:{CHEST_COORDINATES}"
    conn.send(str.encode(config_client))
    while True:
        try:
            data = conn.recv(BUFFER_SIZE)  # Recibe los datos
            reply = data.decode("utf-8")  # Decodifica los datos
            if not data:
                print("Desconexión")
                break
            else:
                position_player = reply.split(":")[1]
                msg_client = reply.split(":")[2]
                print(f"{id_client}: {position_player}:{msg_client}")
            conn.sendall(str.encode(reply))  # Envía los datos
        except:
            break
    print(f"Conexión terminada con el jugador {id_client}")
    current_id -= 1
    conn.close()

# Loop principal
while True:
    client, address = socket_server.accept()  # Acepta la conexión
    print(f"Conexión aceptada de {address[0]}:{address[1]}")
    start_new_thread(threaded_client, (client,))
