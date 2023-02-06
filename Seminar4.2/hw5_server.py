import socket
from _thread import *

host = '127.0.0.1'
port = 1200
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
lsock.bind((host, port))
lsock.listen(50) # в аргументах указываем максимальное число подключений
# lsock.setblocking(False) # останавливает блокировку,нужно для селекторов, при мультитредах неактуально
print(f"Сервер запущен на {(host, port)}")
max_buffer_length = 1024


def receive_from_client(conn_s:socket.socket, addr):
    #теперь начинаем отслеживать сами сообщения
    print(f'conn_s is {conn_s}')
    print(f'port_key gonna be {addr[1]}')
    try:
        while True:
            message = conn_s.recv(max_buffer_length)
            message_to_send = c_users[addr[1]] + message
            #показываем сообщение на сервере
            print ((c_users[addr[1]] + message).decode('utf-8'))
            #и рассылаем по всем сокетам
            broadcast(message_to_send,conn_s, addr[1])
    except KeyboardInterrupt:
        #если ошибки, то отключаем сокет
        clean(addr[1])
        conn.close()


def broadcast(mes, connection,user):
    for key in c_users.copy():
        if key!=user: # шлём всем, кроме самого юзера, чтобы избежать дубликатов в консоли
            try:
                connection.send(mes)
            except:
                # если какая-то ошибка, тоже чистим сокеты и наш словарь
                print(f"ошибка отправки сообщения в {user}")
            finally:
                connection.close()
                clean(user)
                continue


def clean(entry):
    print("Cleaning entry")
    print("before: ",c_users)
    if entry in c_users.copy():
        del c_users[entry]
    print("after: ", c_users)



c_users = {}

# здесь уже делаем "вечный" приемник новых подключений. В отдельную функцию, как я понял, пихать не получится из-за тредов и области видимости
try:
    while True:
        conn,addr= lsock.accept()
        print(f"Новое подключение от {addr}")
        # добавляем в словарь юзеров первое сообщение
        nickname = conn.recv(max_buffer_length)
        c_users[addr[1]] = nickname+b' : ' 
        print(f"{nickname.decode('utf-8')} присоединился к чату")
        conn.send(b"Welcome to the chat!")
        # навешиваем отдельный тред на каждое новое подключение
        start_new_thread(receive_from_client , (conn,addr))
except KeyboardInterrupt:
    print("Shutting down due to keyboard interrupt command")
finally:
    lsock.close() #не похоже, что работает

conn.close()
lsock.close()