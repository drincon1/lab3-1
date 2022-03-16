# Archivo .py con el codigo del cliente
import socket
import os
import threading
# ---ATRIBUTOS---
IP = 'localhost'
PORT = 10000

# ---MÉTODOS---
def thread_function(tup):
	# El cliente se conecta al servidor
	cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	cliente.connect(tup)
	print(f'[CLIENTE {threading.current_thread().getName()}] conectado')
	try:
		# El cliente espera que el servidor le pregunte si quiere empezar la transeferencia de archivos.
		data = cliente.recv(16).decode("utf-8")
		print(f"[CLIENTE {threading.current_thread().getName()}] {data}")
		# Cliente confirma que quiere recibir archivo
		cliente.sendall("OK".encode("utf-8"))
		# Cliente recibe el hash del contenido del archivo
		# TODO

		#Cliente recibe el archvio
		print(f"[CLIENTE {threading.current_thread().getName()}] Esperando el archivo")
		arch = cliente.recv(1024)
		print(f"[CLIENTE {threading.current_thread().getName()}] Archivo recibido")

		# Se calcula el hash del archivo recibido
		# TODO

		# Si no es el mismo se informa y se acaba el proceso. Si es el mismo se guarda el archivo
		# TODO
		ruta = f"archivos_cliente/{threading.current_thread().getName()}-Prueba-0.txt"
		file = open(ruta, "w")
		file.write(arch.decode("utf-8"))
		file.close()
	finally:
		print('closing socket')
		cliente.close()


def main():
	# Cuántos clientes se manejaran
	num_clientes = int(input('¿Cuántos clientes quiere conectados?\n')) + 1
	# Conexión al servidor para la configuración
	set_up = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = (IP,PORT)
	set_up.connect(server_address)
	arch = set_up.recv(2048)
	# Escoger con cuál archivo se va a trabajar
	archivo = input('[1] 100 MB\n[2] 250 MB\n')
	set_up.send(archivo.encode("utf-8"))

	# Se generan la cantidad de clientes deseados de manera concurrente
	for i in range(1, num_clientes): # El máximo no es inclusivo
		cliente_t = threading.Thread(target=thread_function, name="Cliente"+str(i), args=(server_address,))
		cliente_t.start()


if __name__ == "__main__":
    main()
