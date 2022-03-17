# Archivo .py con el codigo del cliente
import socket
import os
import threading
import hashlib
import logging

# ---ATRIBUTOS---
IP = 'localhost'
PORT = 5000

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
		while True:
			arch_recv = cliente.recv(2048).decode("utf-8")
			arch += arch_recv
			if not arch_recv:
				break
		#arch = cliente.recv(8).decode("utf-8")
		print(f"[{threading.current_thread().getName()}] Archivo recibido {arch}")
		# Se calcula el hash del archivo recibido
		hash_calc = hashlib.md5(arch.encode()).hexdigest().encode('utf-8')
		hash_calc =  hash_calc.decode('utf-8')
		print(f"[{threading.current_thread().getName()}] El hash calculado fue {hash_calc}")
		# Si no es el mismo se informa y se acaba el proceso. Si es el mismo se guarda el archivo
		if hash_recv == hash_calc:
			ruta = f"archivos_cliente/{threading.current_thread().getName()}-Prueba-0.txt"
			file = open(ruta, "w")
			file.write(arch)
			file.close()
			print(f"[{threading.current_thread().getName()}] Se ha guardado el archivo")
		else:
			print(f"[{threading.current_thread().getName()}] ¡El archivo recibido ha sido modificado!")
	finally:
		print('closing socket')
		cliente.close()
#----------------------------------------------------------------

def main():
	# Conexión al servidor para la configuración
	set_up = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = (IP,PORT)
	set_up.connect(server_address)
	# Se informa con cuántos clientes se van a trabajar
	num_clientes = int(set_up.recv(2048).decode("utf-8"))

	# Se generan la cantidad de clientes deseados de manera concurrente
	for i in range(1, num_clientes): # El máximo no es inclusivo
		cliente_t = threading.Thread(target=thread_function, name="Cliente"+str(i), args=(server_address,))
		cliente_t.start()


if __name__ == "__main__":
    main()
