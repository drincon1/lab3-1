# Archivo .py con el codigo del servidor
import socket
import os
import threading

IP = 'localhost'
PUERTO = 10000
ADDR = (IP,PUERTO)
FORMAT = "utf-8"
SERVER_DATA_PATH = "server-data"
cont=0

def thread_function(connection,client_address):
	print(f"[SERVIDOR] {client_address} conectado")
	connection.send("Usted se ha conectado exitosamente al servidor".encode(FORMAT))
	while True:
		data=input("> ")
		data = data.split(" ")
		filePath = data[0]
		numClientes = data[1]
		
		with open(f"{filePath}", "r") as f:
			text = f.read()
		fileName = filePath.split("/")[-1]
		send_data = f"{fileName}@{text}"
		if(threading.activeCount()<numClientes):
			break
		if(cont<numClientes):
			conn.send(send_data.encode(FORMAT))
			cont+=1
		


def main():
	print("[SERVIDOR] INICIALIZANDO SERVIDOR")
	servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	servidor.bind(ADDR)
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
