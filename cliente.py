# Este archivo contiene la representacion de los clientes
import socket
import os
import threading

def thread_function(i):
	cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('localhost',10000)
	print('[CLIENTE] connecting too {} port {}'.format(*server_address))
	cliente.connect(server_address)
	try:
		message = b'This is the message. It will be repeated'
		print(f"[CLIENTE {i}] Enviando mensaje")
		cliente.sendall(message)
		amount_received = 0
		amount_expected = len(message)

		while(amount_received < amount_expected):
			data = cliente.recv(16)
			amount_received += len(data)
			print(f'[CLIENTE {i}] Recibi {data}')
	finally:
		print('closing socket')
		cliente.close()


def main():
	#for i in range(1,3): # El máximo no es inclusivo
	cliente_1 = threading.Thread(target=thread_function, args=(1,))
	cliente_2 = threading.Thread(target=thread_function, args=(1,))
	cliente_1.start()
	cliente_2.start()
	#print(f"[CLIENTE {i}]")


if __name__ == "__main__":
    main()
