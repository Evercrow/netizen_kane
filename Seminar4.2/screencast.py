import socket
import threading
from  time import sleep
ya_sock = socket.socket()
addr = ('87.250.250.242',443)
ya_sock.connect(addr)


data_out = b'GET / HTTP/1.1\r\nHost:ya.ru\r\n\r\n'
ya_sock.send(data_out)

data_in = b''
def receiving():
    global data_in
    while True:
        data_chunk = ya_sock.recv(1024)
        data_in = data_in+data_chunk

rec_thread = threading.Thread(target=receiving)
rec_thread.start()


sleep(4)
print(data_in)
ya_sock.close()