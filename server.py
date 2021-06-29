import socket
import threading

class Server:
    def __init__(self):
        self.clients = {}
    def handle_connection(self, conn, addr):
        try:
            name = conn.recv(1024).decode()
            self.clients[conn] = name
            self.broadcast_to_all("[SERVER] {} has connected.".format(name))
            while True:
                msg = conn.recv(2048).decode()
                if msg == "":
                    self.broadcast_to_all("[SERVER] {} has disconnected.".format(name))
                    break
                self.broadcast_to_all("{}: {}".format(name, msg))
        except Exception:
            self.broadcast_to_all("[SERVER] {} has disconnected.".format(name))
            return
    def broadcast_to_all(self, message):
        for sock in self.clients:
            try:
                sock.send(message.encode())
            except BrokenPipeError:
                continue

host = "localhost"
port = 58030
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen()
server = Server()
while True:
    conn, addr = s.accept()
    threading.Thread(target = server.handle_connection, args = (conn,addr,)).start()
