import socket
import select
import threading
import sys

host = "localhost"
port = 58030
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = (host,port)

address = (host,port)
s.connect(address)
name = "user"
s.send(name.encode())

while True:
    sockets_list = [sys.stdin, s] 
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 
    for socks in read_sockets: 
        if socks == s: 
            message = socks.recv(2048).decode()
            message = " ".join(message.split())
            recv_from = message.split(":")[0]
            if not name == recv_from:
                print(message) 
        else: 
            message = sys.stdin.readline() 
            s.send(message.encode()) 
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
            sys.stdout.write("{}: ".format(name)) 
            sys.stdout.write(message) 
            sys.stdout.flush() 
