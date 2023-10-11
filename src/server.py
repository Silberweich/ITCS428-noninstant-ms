from message import Message, createMessage, deserializeMessage, serializeMessage
from reqType import ReqType
from time import sleep
import pickle
import threading
import socket

## Server class
# @brief This class is used to create a server object
class Server():

    servingStatus = True

    def __init__(self, host: str, port: int, listen: int) -> None:
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.bind((self.host, self.port))
            self.sock.listen(listen)
            print(f"[-] Server Started on {self.host}:{self.port}")
        except Exception as e:
            print(f"[-] Server Creation Error:{e}")
    
    def __repr__(self) -> str:
        return f"Server Listening on {self.host}:{self.port} | {self.sock}"
    
    def setServingStatus(self, status: bool) -> None:
        self.servingStatus = status
        return None
    
    def startServing(self) -> None:
        while self.servingStatus:
            conn, addr = self.sock.accept()
            print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
            # threading.Thread(target=self.__handleConnection, args=(conn, addr)).start()
            match conn.recv(8):
                case ReqType.STORE.value:
                    self.__modeStore(conn)
                case ReqType.REQ_ALL.value:
                    self.__modeSendAll(conn)
                case ReqType.REQ_NEW.value:
                    self.__modeSendNew(conn)
                case _:
                    print("[-] Invalid Request Type")
                    sleep(5)

    def __modeStore(self, conn) -> None:
        print("[*] in store mode")
        conn.send(ReqType.ACK.value)
        print("[*] ACK sent to", conn.getpeername())
        data = deserializeMessage(conn.recv(2048))
        print("[*] Data received from", conn.getpeername())
        print(f"[*] Data:{data}")
        sleep(2)
        return None

    def __modeSendAll(self, conn) -> None:
        print("[*] in send all mode")
        conn.send(ReqType.ACK.value)
        sleep(2)
        return None
    
    def __modeSendNew(self, conn) -> None:
        print("[*] in send all mode")
        conn.send(ReqType.ACK.value)
        sleep(2)
        return None
    
# Testing for this file
# if __name__ == "__main__":
#     server = Server("127.0.0.1", 8080, 1)
#     server.startServing()