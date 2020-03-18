import socket, json, os


class network:
    def __init__(self):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketqueue = []

    def bindserver(self, ip, port):
        self.socket_obj.bind((ip, port))
        self.socket_obj.listen(4)

    def send(self, message, client):
        message = bytes(json.dumps(message) + "\n", "UTF-8")
        client.send(message)

    def receive(self, client):
        if self.socketqueue == [""]:
            self.socketqueue = []
        if not self.socketqueue == []:
            message = self.socketqueue.pop(0)
        
        else:
        
            message = client.recv(1024).decode("UTF-8")
            if "\\n" in message:
                message = message.replace("\\n", "")
            splitted = message.split("\n")

            if len(splitted) == 2:
                message = splitted[0]

            else:
                self.socketqueue = splitted
                message = self.socketqueue.pop(0)
                
        #print("message: " + str(message))#PRIMAL LOGGING METHOD
        try:
            message = json.loads(message)

        except json.decoder.JSONDecodeError:
            print("birisinin bağlantısı koptu ya da oyun çöktü ya da ikisi de :(")#TODO: remove
            os._exit(0)


        return message

    def accept(self):
        client, adress = self.socket_obj.accept()
        return client, adress

    def connect(self, ip, port):#CLIENT METHOD
        self.socket_obj.connect((ip, port))

    def receive_client(self):#CLIENT METHOD
        return self.receive(self.socket_obj)

    def send_client(self, message):#CLIENT METHOD
        self.send(message, self.socket_obj)
