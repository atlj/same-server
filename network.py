import socket, json


class network:
    def __init__(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bindserver(self, ip, port):
        self.socket_obj.bind((ip, port))
        self.socket_obj.listen(4)

    def send(self, message, client):
        message = bytes(json.dumps(message), "UTF-8")
        client.send(message)

    def receive(self, client):
        message = client.recv(1024).decode("UTF-8")
        message = json.loads(message)
        return message

    def accept(self):
        client, adress = self.socket_obj.accept()
        return client, adress
