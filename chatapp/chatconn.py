import socket, threading, requests

from chatapp.constants import Constants   
from .windowgui.timers import RealTimer 
from .util import ConnIDTaken, ConnInvalidIP, ConnPortTaken, ConnRefused

def _get_private_ip():
    if Constants.HAS_INTERNET:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(('10.255.255.255', 1))
        return s.getsockname()[0]
    return ""

def _get_public_ip():
    if Constants.HAS_INTERNET:
        return requests.get("https://api.ipify.org").text
    return ""

class ChatConn:
    PORT = 5007

    IP_PRIVATE = _get_private_ip()
    IP_PUBLIC = _get_public_ip()

    HEADER = 16

    LISTENING_TIMEOUT = 0.2

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
        self.connected = False
        self.out_queue = []
        self.in_queue = []
        

        if self.type == "server":
            try:
                self.socket.bind(self.addr)
                self.socket.settimeout(self.LISTENING_TIMEOUT)
            except OSError:
                raise ConnPortTaken("cannot host two servers on the same computer")
            print("[SERVER] bound to address")
            threading.Thread(target=self._run_server).start()


        elif self.type == "client":
            try:
                self.socket.connect(self.addr)
            except ConnectionRefusedError:
                raise ConnRefused(f"client unable to find server at IP \"{self.addr[0]}\"")
            except socket.gaierror:
                raise ConnInvalidIP(f"\"{self.addr[0]}\" is not a valid IP")
            except OSError:
                raise ConnInvalidIP(f"\"{self.addr[0]}\" is not a valid IP")
            
            msg_type, conn_id = self._recv(self.socket)
            if conn_id == self.id:
                self._send(self.socket, "", self.MsgType.BREAK)
                raise ConnIDTaken("ChatConn attempted to join a ChatConn with same id")
            self._send(self.socket, self.id, self.MsgType.INIT)
            print(f"[CLIENT] connected to server: {conn_id}")
            threading.Thread(target=self._server_handler, args=[conn_id]).start()
    
    def _send(self, conn, data, msg_type):
        data = data.encode()
        data_len = len(data)
        meta = f"{data_len},{msg_type}".encode()
        meta += b' ' * (self.HEADER - len(meta))
        conn.send(meta)
        conn.send(data)

    def _recv(self, conn):
        try:
            meta = conn.recv(self.HEADER).decode()
        except ConnectionResetError:
            self.running = False
            raise ConnectionResetError("shit me connection rest")
        meta = meta.split(",")
        data_len, msg_type = int(meta[0]), int(meta[1])
        data = conn.recv(data_len).decode()
        return msg_type, data
    
    def _run_server(self):
        self.socket.listen()
        while self.running:
            try:
                conn, addr = socket.accept()
            except socket.timeout:
                pass
            else:
                threading.Thread(target=self._client_handler, args=[conn]).start()
                if threading.active_count() > 1:
                    self.connected = True
        self.socket.close()
        

    def _client_handler(self, conn):
        self._send(conn, self.id, self.MsgType.INIT)
  
        msg_type, data = self._recv(conn)
        if msg_type == self.MsgType.BREAK:
            return None
        conn_id = data

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
        
    

    
    def _server_handler(self, conn_id):
        self.connected = True
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
        self.connected = False


