# Archivo .py con el codigo del servidor
import socket
import os
import threading
import hashlib
import logging
from datetime import datetime
import time

#IP = "localhost"
IP = "192.168.124.139"
PUERTO = 5000
num_clientes = 0
ruta_archivo = ""
tamano = 0

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
			print(f'[SERVIDOR] Enviando el archivo a {threading.current_thread().getName()}')
			# Se inicia el cronómetro
			starttime = time.time()
			lasttime = starttime
			# Serviro manda el archivo escogido
			bytes_e=connection.send(text.encode("utf-8"))
			print(f'[SERVIDOR] Archivo enviado a {threading.current_thread().getName()}')
			# Escribir el archivo log
			entre_exitosa =""
			if bytes_e>=tamano:
				# Se para el cronómetro
				laptime = round((time.time() - lasttime), 2)
				entre_exitosa ="SI"
			else:
				entre_exitosa ="NO"
			now = datetime.today()
			ruta = f"Logs/S-{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}.txt"
			file = open(ruta, "w")
			file.write(f"Nombre del archivo: {ruta_archivo[-9:]}\nTamaño: {ruta_archivo[-9:-4]}\nCliente: {threading.current_thread().getName()}\nEntrega Exitosa: {entre_exitosa}\nTiempo tomado: {laptime}")
			file.close()
		else:
			print('[SERVIDOR] El cliente no desea recibir archivos')
	finally:
		connection.close()
#----------------------------------------------------------------

# -------CONFIGURACIÓN DEL EJERCICIO-------
# Definir con cuál archivo se trabajará
res_archivo = input('¿Cual archivo desea recibir sus clientes?\n[1] 100 MB\n[2] 250 MB\n')
#if para establecer la ruta
if int(res_archivo) == 1:
	ruta_archivo = "archivos_servidor/100MB.txt"
	tamano = 100000000
elif int(res_archivo) == 2:
	ruta_archivo = "archivos_servidor/250MB.txt"
	tamano = 250000000
else:
	ruta_archivo = "archivos_servidor/prueba.txt"

# Cuántos clientes se manejaran
num_clientes  = int(input('¿Cuántos clientes quiere conectados?\nOpciones válidas: 1,5,10\n')) + 1
print(f"[SERVIDOR] Se recibió {num_clientes-1} clientes")

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
# Confirmación de la aplicación cliente
conn.recv(1024).decode('utf-8')
# Enviar a la aplicación cliente el archivo que se va a usar
conn.send(res_archivo.encode('utf-8'))
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
