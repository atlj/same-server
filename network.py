import socket
from threading import Thread

socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class network:
    def __init__(self):
        pass

    def bindserver(self, ip, port):
        socket_obj.bind(ip, port)

    def client_handler(self):
        client, addr = socket_obj.accept()
