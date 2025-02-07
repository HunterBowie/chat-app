import socket, threading, requests

from .constants import Constants   
from .windowgui.timers import RealTimer 
from .exceptions import ConnIDTaken, ConnInvalidIP, ConnPortTaken, ConnRefused

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
    """Repersents the client/server connection."""
    PORT = 5007

    IP_PRIVATE = _get_private_ip()
    IP_PUBLIC = _get_public_ip()

    HEADER = 16

    SOCKET_TIMEOUT = 0.2

    class MsgType:
        """Repersents the type of msg being sent."""
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
        self.connections = []
        self.send_queue = []
        self.recv_queue = []

        if self.type == "server":
            try:
                self.socket.bind(self.addr)
                self.socket.settimeout(self.SOCKET_TIMEOUT)
            except OSError:
                raise ConnPortTaken("cannot host two servers on the same computer")
            print("[SERVER] bound to address")
            threading.Thread(target=self._run_server).start()


        elif self.type == "client":
            try:
                print("got here")
                self.socket.settimeout(self.SOCKET_TIMEOUT)
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
    
    def has_msg(self):
        if self.recv_queue:
            return True
        return False

    def get_msg(self):
        # print(f"[GENERAL] new msg pulled to chatbox: {self.recv_queue[-1]}")
        return self.recv_queue.pop(-1)

    def send_msg(self, content):
        self.send_queue.append((content, self.connections.copy()))
    
    def _send(self, conn, data, msg_type: int):
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
            raise ConnectionResetError("connection reset")
        meta = meta.split(",")
        data_len, msg_type = int(meta[0]), int(meta[1])
        data = conn.recv(data_len).decode()
        return msg_type, data
    
    def _run_server(self):
        self.socket.listen()
        while self.running:
            try:
                conn, addr = self.socket.accept()
            except socket.timeout:
                pass
            else:
                threading.Thread(target=self._client_handler, args=[conn]).start()
        self.socket.close()
        
    def _client_handler(self, conn):
        
        self._send(conn, self.id, self.MsgType.INIT)

        msg_type, data = self._recv(conn)
        if msg_type == self.MsgType.BREAK:
            return None
        conn_id = data

        self.connections.append(conn_id)

        conn.settimeout(self.SOCKET_TIMEOUT)

        print(f"[SERVER] new client {conn_id}")

        while True:
            try:
                msg_type, data = self._recv(conn)
            except socket.timeout:
                continue


            if msg_type == self.MsgType.CHAT:
                print("[SERVER] recived msg")
                self.recv_queue.append({"id": conn_id, "content": data})
                if len(self.connections) > 1:
                    mod_connections = self.connections.copy()
                    mod_connections.remove(conn_id)
                    self.send_queue.append((data, mod_connections))

            elif msg_type == self.MsgType.BREAK:
                print("[SERVER] client disconnect")     
                break
            
            if not self.running:
                self._send(conn, "", self.MsgType.BREAK)
                break
            
            msg_item = None
            delete_item = False
            for new_item in self.send_queue:
                if conn_id in new_item[1]:
                    msg_item = new_item
                    msg_item[1].remove(conn_id)
                    if len(msg_item[1]) == 0:
                        delete_item = True
            if delete_item:
                self.send_queue.remove(msg_item)
            
            # print(f"[SERVER] Preparing msg item {msg_item} from {self.send_queue}")

            excepting = True
            while excepting:
                try:
                    if msg_item is not None:
                        self._send(conn, msg_item[0], self.MsgType.CHAT)
                        print(f"[SERVER] sent msg {msg_item[0]}")
                    else:
                        self._send(conn, "", self.MsgType.EMPTY)
                except socket.timeout:
                    pass

                else:
                    excepting = False
                
                if not self.running:
                    self.connections.remove(conn_id)
                    return None

        self.connections.remove(conn_id)

    def _server_handler(self, conn_id):
        self.connections.append(conn_id)
        while self.running:
            msg_item = None
            delete_item = False
            for new_item in self.send_queue:
                if conn_id in new_item[1]:
                    msg_item = new_item
                    if len(msg_item[1]) == 1:
                        delete_item = True
            if delete_item:
                self.send_queue.remove(msg_item)
            
            # print(f"[CLIENT] Preparing msg item {msg_item} from {self.send_queue}")

            excepting = True
            while excepting:
                try:
                    if msg_item is not None:
                        self._send(self.socket, msg_item[0], self.MsgType.CHAT)
                        print(f"[CLIENT] sent msg {msg_item[0]}")
                    else:
                        self._send(self.socket, "", self.MsgType.EMPTY)
                except socket.timeout:
                    pass

                else:
                    excepting = False
            
            excepting = True
            while excepting:
                try:
                    msg_type, data = self._recv(self.socket)
                except socket.timeout:
                    pass
                else:
                    excepting = False
            if msg_type == self.MsgType.CHAT:
                print("[CLIENT] recieved msg")
                self.recv_queue.append({"id": conn_id, "content": data})
            elif msg_type == self.MsgType.BREAK:
                print("[CLIENT] server disconnected")
                break
        else:
            self._send(self.socket, "", self.MsgType.BREAK)
            
        self.socket.close()
        self.connections.remove(conn_id)


