# Archivo .py con el codigo del servidor
import socket
import os
import threading

IP = 'localhost'
PUERTO = 10000

def thread_function(connection,client_address):
	print(f"[SERVIDOR] {client_address} conectado")
	#
	connection.send("[SERVIDOR] ¿Desea comenzar la conexión?".encode("utf-8"))
	#while True:
	data = connection.recv(16)
	if data:
		print(f'[SERVIDOR] Se ha recibido {data}')
		# Serviro manda el archivo escogido
		with open("archivos_servidor/prueba.txt", "r") as f:
			text = f.read()
		print('[SERVIDOR] Enviando el archivo')
		connection.send(text.encode("utf-8"))

	else:
		print('no data from')
		#break


def main():


	print("[SERVIDOR] INICIALIZANDO SERVIDOR")
	servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = (IP,PUERTO)
	try:
		servidor.bind(server_address)
	except servidor.error as e:
		print(str(e))

	print(f"[SERVIDOR] Escuchando en {IP}:{PUERTO}")
	servidor.listen()

	print("[SERVIDOR] ESPERANDO CONEXIONES")
	conn,set_up = servidor.accept()
	conn.send('¿Cual archivo desea recibir sus clientes?'.encode("utf-8"))
	archivo = conn.recv(2048)


	while True:
		connection, client_address = servidor.accept()
		cliente = threading.Thread(target=thread_function, args=(connection,client_address))
		cliente.start()
		print(f"[CONEXIONES ACTIVAS] {threading.activeCount() - 1}")


if __name__ == "__main__":
    main()
