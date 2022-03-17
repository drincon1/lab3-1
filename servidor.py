# Archivo .py con el codigo del servidor
import socket
import os
import threading
import hashlib
import logging

IP = 'localhost'
PUERTO = 5000
num_clientes = 0
ruta_archivo = ""

#----------------------------------------------------------------
def thread_function(connection,client_address):
	# Informa el puerto del cliente
	print(f"[SERVIDOR] {client_address} conectado")
	#Pregunta si desea comenzar la transferencia de archivos
	connection.send("[SERVIDOR] ¿Desea comenzar la transferencia de archivos?".encode("utf-8"))
	data = connection.recv(1024).decode("utf-8")
	try:
		print(f'[SERVIDOR] Se ha recibido {data}')
		if data == "OK":
		# Se busca el archivo deseado
			with open(ruta_archivo, "r") as f:
				text = f.read()
		# Se calcula el valor de hash al contenido del archivo
			f_hash = hashlib.md5(text.encode()).hexdigest().encode('utf-8')
			print("[SERVIDOR] El hash calculado fue",f_hash)
		# Se envia el hash calculado
			connection.send(f_hash)
		# Se espera a todos los clientes
			print(f"[SERVIDOR] {threading.current_thread().getName()} esperando")
			barrier.wait()
		# Se envia el archivo al cliente
			print('[SERVIDOR] Enviando el archivo')
		# Serviro manda el archivo escogido
			connection.send(text.encode("utf-8"))
		else:
			print('[SERVIDOR] El cliente no desea recibir archivos')
	finally:
		connection.close()
#----------------------------------------------------------------



# Definir con cuál archivo se trabajará
# CONFIGURACIÓN DEL EJERCICIO (¿Cuál archivo se transmitirá?)
res_archivo = input('¿Cual archivo desea recibir sus clientes?\n[1] 100 MB\n[2] 250 MB\n')
#if para establecer la ruta
if int(res_archivo) == 1:
	ruta_archivo = "archivos_servidor/100MB.txt"
elif int(res_archivo) == 2:
	ruta_archivo = "archivos_servidor/250MB.txt"
else:
	ruta_archivo = "archivos_servidor/prueba.txt"

# Cuántos clientes se manejaran
num_clientes  = int(input('¿Cuántos clientes quiere conectados?\n')) + 1

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
print("[SERVIDOR] COMIENCE LA APLICACIÓN CLIENTE.PY")
servidor.listen()

#Se habilita el servidor para hacer la configuración con la aplicación cliente
conn,set_up = servidor.accept()
# Enviar a la aplicación cliente cuantos clientes tendrá que simular concurrentemente
conn.send(str(num_clientes).encode("utf-8"))
conn.close()
num_clientes = num_clientes - 1
barrier = threading.Barrier(num_clientes)


print("[SERVIDOR] ESPERANDO CONEXIONES")
i = 1
# Ciclo infinito para siempre estar escuchando conexiones de los clientes
while True:
	# Aceptar la conexión del cliente
	connection, client_address = servidor.accept()
	# Manejar la conexión como un hilo, i.e., concurrente
	cliente = threading.Thread(target=thread_function, name="Cliente "+str(i),args=(connection,client_address))
	# Comenzar el hilo <- Comunicación servidor-cliente
	cliente.start()
	i = i+1
	print(f"[CONEXIONES ACTIVAS] {threading.activeCount() - 1}")
