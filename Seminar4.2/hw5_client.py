# 1.Напишите свою программу сервер и запустите её.
# 2.Запустите несколько клиентов. Сымитируйте чат.
# 3.Отправьте мне код написанного сервера 
# (можете через github, если удобно или прямо здесь в txt формате) и скриншоты работающего чата.
# 4.Отследите сокеты с помощью команды netstat. 
# (тоже пришлите скриншот именно сокетов вашего чата) . 
# статья в помощь - https://realpython.com/python-sockets/#echo-server


import socket
import threading
from time import sleep
max_buffer_length = 1024

def connect_human_client():
    user_name = input("Enter your username:")
    my_sock = socket.socket()
    server = ('127.0.0.1',1200) 
    my_sock.connect(server)
    my_sock.send(user_name.encode(encoding='ascii'))

    
    def reading_chat():
        while True:
            new_mess = my_sock.recv(max_buffer_length)
            sleep(1)
            if len(new_mess) !=0 : print(new_mess)



    def chatting():
        
        try:
            while True:
                message = input()
                if message == 'exit': #ручной выход, если комбинация не работает
                    my_sock.close()
                    break
                my_sock.send(message.encode(encoding='ascii'))
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            my_sock.close()

    send_thread = threading.Thread(target=chatting)
    rec_thread = threading.Thread(target=reading_chat)
    rec_thread.start()
    send_thread.start()

    
    








connect_human_client() # прекращение по ctr+c





