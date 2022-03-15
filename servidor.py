# Archivo .py con el codigo del servidor
import socket
import os
import threading

IP = 'localhost'
PUERTO = 10000

def thread_function(connection,client_address):
	print(f"[SERVIDOR] {client_address} conectado")
	connection.send("Usted se ha conectado exitosamente al servidor")
	while True:
		data = connection.recv(16)
		print('received{!r}'.format(data))
		if data:
			print('sending back to the client')
			connection.sendall(data)
		else:
			print('no data from', client_address)
			break


def main():
	print("[SERVIDOR] INICIALIZANDO SERVIDOR")
	servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = (IP,PUERTO)
	servidor.bind(server_address)
	servidor.listen()
	print(f"[SERVIDOR] Servidor está escuchando en {IP}:{PUERTO}")

	print("[SERVIDOR] ESPERANDO CONEXIONES")
	while True:
		connection, client_address = servidor.accept()
		cliente = threading.Thread(target=thread_function, args=(connection,client_address))
		cliente.start()
		print(f"[CONEXIONES ACTIVAS] {threading.activeCount() - 1}")


if __name__ == "__main__":
    main()
