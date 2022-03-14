# Archivo .py con el codigo del servidor
import socket
import sys

#Creacion de un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Unir al socket con el puerto
server_address = ('localhost',10000)
print('Starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

sock.listen(1)

while True:
	print('Waiting for a conection')
	connection, client_address = sock.accept()
	try:
		print('connection from', client_address)
	finally:
		connection.close()

