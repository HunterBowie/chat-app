import socket

class Protocol:
    PORT = 5007

    class MsgType:
        INIT = 0
        BREAK = 1


class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((socket.gethostbyname(socket.gethostname()), Protocol.PORT))


class Client:
    def __init__(self, ip):
        self.socket = socket.connect(ip)
