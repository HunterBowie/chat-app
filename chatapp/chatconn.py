import socket, threading, requests   
from .windowgui.timers import RealTimer 

def _get_private_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    s.connect(('10.255.255.255', 1))
    return s.getsockname()[0]

def _get_public_ip():
    return requests.get("https://api.ipify.org").text

class ChatConn:
    PORT = 5007

    IP_PRIVATE = _get_private_ip()
    IP_PUBLIC = _get_public_ip()

    HEADER = 16

    class MsgType:
        INIT = 0
        BREAK = 1
        CHAT = 2
        EMPTY = 3
    
   

    def __init__(self, type, ip, id):
        self.id = id
        self.type = type
        self.addr = (ip, self.PORT)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        self.out_queue = []
        self.in_queue = []

        if self.type == "server":
            self.socket.bind(self.addr)
            print("[SERVER] bound to address")
            threading.Thread(target=self._run_server).start()


        elif self.type == "client":
            self.socket.connect(self.addr)
            print("[CLIENT] connected to server")
            threading.Thread(target=self._server_handler).start()
    
    def _send(self, conn, data, msg_type):
        data = data.encode()
        data_len = len(data)
        meta = f"{data_len},{msg_type}".encode()
        meta += b' ' * (self.HEADER - len(meta))
        conn.send(meta)
        conn.send(data)

    def _recv(self, conn):
        meta = conn.recv(self.HEADER).decode()
        meta = meta.split(",")
        data_len, msg_type = int(meta[0]), int(meta[1])
        data = conn.recv(data_len).decode()
        return msg_type, data
    
    def _run_server(self):
        self.socket.listen()
        while self.running:
            conn, _ = self.socket.accept()
            threading.Thread(target=self._client_handler, args=[conn]).start()
        self.socket.close()
        

    def _client_handler(self, conn):
        msg_type, conn_id = self._recv(conn)
        self._send(conn, self.id, self.MsgType.INIT)

        timer = RealTimer()
        timer.start()

        print(f"[SERVER] new client {conn_id}")

        while self.running:
        
            msg_type, data = self._recv(conn)
            if msg_type == self.MsgType.CHAT:
                print("[SERVER] recived msg")
                self.in_queue.append({"id": conn_id, "content": data})
            elif msg_type == self.MsgType.BREAK:
                print("[SERVER] client disconnect")
                return None
            
            
            if self.out_queue:
                self._send(conn, self.out_queue.pop(0), self.MsgType.CHAT)
                print("[SERVER] sent msg")
            else:
                self._send(conn, "", self.MsgType.EMPTY)
    

    
    def _server_handler(self):
        self._send(self.socket, self.id, self.MsgType.INIT)
  
        msg_type, data = self._recv(self.socket)
        conn_id = data

        while self.running:
            if self.out_queue:
                self._send(self.socket, self.out_queue.pop(0), self.MsgType.CHAT)
                print("[CLIENT] sent msg")
            else:
                self._send(self.socket, "", self.MsgType.EMPTY)
            
            msg_type, data = self._recv(self.socket)
            if msg_type == self.MsgType.CHAT:
                print("[CLIENT] recieved msg")
                self.in_queue.append({"id": conn_id, "content": data})
            if msg_type == self.MsgType.BREAK:
                print("[CLIENT] server disconnected")
                break
        else:
            self._send(self.socket, "", self.MsgType.BREAK)
            
        self.socket.close()


