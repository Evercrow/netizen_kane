import socket
import threading
import sys
from  time import sleep
max_buffer_length = 1024

def connect_bot(n):
    my_sock = socket.socket()
    addr = ('127.0.0.1',1200)
    my_sock.connect(addr)

    def spam(num:int):
        my_sock.send(f"Yabot{num}".encode(encoding='ascii'))


        def timekill():
            sleep(160)
            my_sock.close()
        stop = threading.Thread(target=timekill)
        stop.start()


        while True:
            my_sock.send(b"I vse za odnogo!")
            sleep(4)

        

    out = threading.Thread(target=spam, args=(n,))
   
    out.start()
    

bot_num=int(sys.argv[1])
connect_bot(bot_num)

