# Задание:
# Необходимо написать программу-клиент, которая будет цепляться к вашему серверу в Интернете
# ip-address: 158.160.20.210, port: 55555
# После того как соединение произошло, первое сообщение будет ником пользователя, 
# а далее, любое отправленное сообщение будет транслироваться другим клиентам.

import socket
import threading
from time import sleep
my_sock = socket.socket()
addr = ('158.160.20.210',55555)
my_sock.connect(addr)


data_out = b'My nick'
my_sock.send(data_out)

data_in = b''
def receiving():
    global data_in
    while True:
        data_chunk = my_sock.recv(1024)
        data_in = data_in+data_chunk

rec_thread = threading.Thread(target=receiving)
rec_thread.start()


sleep(4)
print(data_in)
my_sock.close()