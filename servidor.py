# Archivo .py con el codigo del servidor
import socket
import os
import threading

IP = 'localhost'
PUERTO = 10000

def thread_function(connection,client_address):
	# Informa el puerto del cliente
	print(f"[SERVIDOR] {client_address} conectado")
	#Pregunta si desea comenzar la transferencia de archivos
	connection.send("[SERVIDOR] ¿Desea comenzar la transferencia de archivos?".encode("utf-8"))

	#Recibe la respuesta del cliente si desea o no recibir los archivos
	data = connection.recv(16)
	print(f'[SERVIDOR] Se ha recibido {data}')
	if data:
		# Se busca el archivo deseado
		# TODO


		with open("archivos_servidor/prueba.txt", "r") as f:
			text = f.read()
		# Se calcula el valor de hash al contenido del archivo
		# TODO
		# Se envia el hash calculado
		# TODO

		# Se espera a todos los clientes
		# TODO

		# Se envia el archivo al cliente
		print('[SERVIDOR] Enviando el archivo')
		# Serviro manda el archivo escogido
		connection.send(text.encode("utf-8"))

	else:
		print('[SERVIDOR] El cliente no desea recibir archivos')


def main():
	# Se inicializa el servidor
	print("[SERVIDOR] INICIALIZANDO SERVIDOR")
	servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = (IP,PUERTO)
	try:
		servidor.bind(server_address)
	except servidor.error as e:
		print(str(e))

	# Se habilita el servidor para escuchar
	print(f"[SERVIDOR] Escuchando en {IP}:{PUERTO}")
	servidor.listen()
	# CONFIGURACIÓN DEL EJERCICIO (¿Cuál archivo se transmitirá?)
	#Se habilita el servidor para aceptar la conexión para escoger el archvio
	print("[SERVIDOR] ESPERANDO CONEXIONES")
	conn,set_up = servidor.accept()
	conn.send('¿Cual archivo desea recibir sus clientes?'.encode("utf-8"))
	archivo = conn.recv(2048)

	# Ciclo infinito para siempre estar escuchando conexiones de los clientes
	while True:
		# Aceptar la conexión del cliente
		connection, client_address = servidor.accept()
		# Manejar la conexión como un hilo, i.e., concurrente
		cliente = threading.Thread(target=thread_function, args=(connection,client_address))
		# Comenzar el hilo <- Comunicación servidor-cliente
		cliente.start()
		print(f"[CONEXIONES ACTIVAS] {threading.activeCount() - 1}")


if __name__ == "__main__":
    main()
