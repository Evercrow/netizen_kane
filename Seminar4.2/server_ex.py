'''
Это код для простого эхо-сервера. Ограничение -что ограничен одним подключением от клиента
(после сессии c одним клиентом автоматически завершает работу за счет инкапсуляции внутри with)

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 1200  # Port to listen on (non-privileged ports are > 1023)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
    #указание типа имени хоста, указание типа протокола соединения для порта , инкапсуляция метода(не нужно писать close())
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept() # на accept выполнение кода сервера останавливается, пока не установится соединение
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024) 
            if not data:
                break
            conn.sendall(data) 
        # sendall отправляет все биты, пока они не закончатся внутри переменной, потом возвращает None,
        #по которому мы делаем break цикла. Т.е. пока не отправит все сообщение клиента обратно, эхо-сервер не закроется
        #но здесь прием от клиента все равно ограничен буфером в 1024 байта(бита?)
'''

##Нам же понадобится сервер для нескольких подключений. Можно реализовать за счет множества тредов, но 
# в статье предлагают использовать библиотеку selectors https://realpython.com/python-sockets/#echo-server

import socket
import selectors
import types


#инициализация сервера и слушающего сокета
sel = selectors.DefaultSelector()
# host, port = sys.argv[1], int(sys.argv[2])  # передаем в консоли аргументы, имя хоста и номер порта
host = '127.0.0.1'
port = 1200
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
lsock.bind((host, port))
lsock.listen()
print(f"Сервер запущен на {(host, port)}")
lsock.setblocking(False) # отлючает ожидание программы(блокировка) на .accept(), .connect(), .send(), and .recv()
sel.register(lsock, selectors.EVENT_READ, data=None) # выбираем сокет и какие событя будем на нем мониторить(ЧТЕНИЕ)

users = []
# Прием подключений
def accept_wrapper(sock):
    conn, addr = sock.accept()  # сокет сервера должен быть готов  за счет селектора перед вызовом
    print(f"Новое подключение от {addr}")
    conn.setblocking(False)

    nickname = conn.recv(1024) 
    users.append((addr[1],nickname + b' : '))
    # print(nickname) # debug print
    # print(users[-1]) # debug print
    print(f"{nickname.decode('utf-8')} присоединился к чату")
    conn.send(b"Welcome to the chat!")
    data = types.SimpleNamespace(addr=addr, inb=b"",identity=users[-1], outb=b"") #создание бинарных переменных для след.функции
    events = selectors.EVENT_READ | selectors.EVENT_WRITE #запись через OR, перечисление регистрируемых событий для селектора, ЧТЕНИЕ и ЗАПИСЬ
    sel.register(conn, events, data=data)

# Сбор и рассылка лога чата(сообщений от клиентов)
def service_connection(key, mask):
    #разбиваем SelectorKey на переменные:
    sock = key.fileobj 
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024) 
        if recv_data:
            data.outb += recv_data
            # print(recv_data) # debug print
        else: # закрываем сокет и убираем из селектора, если такой хост больше не считывает инфу(не шлет ACK сессии ?)
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Sending {data.outb!r} to {data.addr}")
            data.outb = data.identity[1] + data.outb
            for listener in events:
                if listener[0].fileobj != sock: #отправляем всем слушаюшим сокетам кроме говорящего
                    listener[0].fileobj.send(data.outb)  # Should be ready to write
            #data.outb = data.outb[sent:] # чистим буфер отправки в чат по числу отосланных байтов
            data.outb = b""




# Цикл обработки подключений
try:
    while True:
        events = sel.select(timeout=None) # блокируется до каждого нового подключения(интерфейса)
        for key, mask in events: # key - это объекты сокета, а mask - битовые коды готовых событий
            if key.data is None:  # незнакомый сокет кидаем в accept
                accept_wrapper(key.fileobj)
            else:           # иначе обмениваемся информацией по send-recv
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()



# socket.setdefaulttimeout(120) # таймаут новых объектов внутри(?) сокета(подключений и методов типа accept)
