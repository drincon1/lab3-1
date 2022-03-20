# Archivo .py con el codigo del cliente
import socket
import os
import threading
import hashlib
import logging
from datetime import datetime
import time

# ---ATRIBUTOS---
#IP = "localhost"
IP = "192.168.124.139"
PORT = 5000
prueba = ""
ruta_archivo = ""
tamano = 0

#----------------------------------------------------------------
def thread_function(tup):
	# El cliente se conecta al servidor
	cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	cliente.connect(tup)
	print(f'[{threading.current_thread().getName()}] conectado')
	try:
		# El cliente espera que el servidor le pregunte si quiere empezar la transeferencia de archivos.
		data = cliente.recv(1024).decode("utf-8")

		print(f"[{threading.current_thread().getName()}] {data}")
		# Cliente confirma que quiere recibir archivo
		cliente.send("OK".encode("utf-8"))
		# Cliente recibe el hash del contenido del archivo
		hash_recv = cliente.recv(1024).decode("utf-8")
		print(f"[{threading.current_thread().getName()}] Recibió el hash {hash_recv}")
		#Cliente recibe el archvio
		print(f"[{threading.current_thread().getName()}] Esperando el archivo")
		arch = ""
		print(f"[{threading.current_thread().getName()}] Recibiendo archivo")
		starttime = time.time()
		lasttime = starttime
		while True:
			arch_recv = cliente.recv(4096).decode("utf-8")
			if not arch_recv:
				break
			arch += arch_recv
			#print(f"Tamaño del archivo recibido: {len(arch_recv)}")
		#arch = cliente.recv(8).decode("utf-8")
		print(f"[{threading.current_thread().getName()}] Archivo recibido")
		# Se calcula el hash del archivo recibido
		hash_calc = hashlib.md5(arch.encode()).hexdigest().encode('utf-8')
		hash_calc =  hash_calc.decode('utf-8')
		print(f"[{threading.current_thread().getName()}] El hash calculado fue {hash_calc}")
		# Si no es el mismo se informa y se acaba el proceso. Si es el mismo se guarda el archivo
		entre_exitosa = ""
		if hash_recv == hash_calc:
			laptime = round((time.time() - lasttime), 2)
			entre_exitosa = "SI"
			ruta = f"ArchivosRecibidos/{threading.current_thread().getName()}-{prueba}.txt"
			file = open(ruta, "w")
			file.write(arch)
			file.close()
			print(f"[{threading.current_thread().getName()}] Se ha guardado el archivo")
		else:
			entre_exitosa = "NO"
			print(f"[{threading.current_thread().getName()}] ¡El archivo recibido ha sido modificado!")

		now = datetime.today()
		ruta = f"Logs/C-{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}.txt"
		file = open(ruta, "w")
		file.write(f"Nombre del archivo: {ruta_archivo[-9:]}\nTamaño: {ruta_archivo[-9:-4]}\nCliente: {threading.current_thread().getName()}\nEntrega Exitosa: {entre_exitosa}\nTiempo tomado: {laptime}")
		file.close()
	finally:
		print('closing socket')
		cliente.close()
#----------------------------------------------------------------


# Conexión al servidor para la configuración
set_up = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (IP,PORT)
set_up.connect(server_address)
# Se informa con cuántos clientes se van a trabajar
num_clientes = int(set_up.recv(2).decode("utf-8"))
set_up.send("OK".encode("utf-8"))
archivo = set_up.recv(8).decode("utf-8")
set_up.close()

if int(archivo) == 1:
	ruta_archivo = "archivos_servidor/100MB.txt"
	tamano = 100000000
elif int(archivo) == 2:
	ruta_archivo = "archivos_servidor/250MB.txt"
	tamano = 250000000
else:
	ruta_archivo = "archivos_servidor/prueba.txt"

prueba = f"Prueba-{num_clientes-1}"
print(f"[APP.CLIENTE] Número de clientes a crear:{num_clientes-1}")
# Se generan la cantidad de clientes deseados de manera concurrente
for i in range(1, num_clientes): # El máximo no es inclusivo
	cliente_t = threading.Thread(target=thread_function, name="Cliente"+str(i), args=(server_address,))
	cliente_t.start()
