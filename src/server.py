from src.message import Message, createMessage, deserializeMessage, serializeMessage
from src.storage import StorageSolution
from src.reqType import ReqType

from time import sleep
from pathlib import Path
import threading
import socket

## Server class
# @brief This class is used to create a server object
class Server():

    servingStatus = True

    def __init__(self, host: str, port: int, listen: int, file: Path) -> None:
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.bind((self.host, self.port))
            self.sock.listen(listen)
            print(f"[-] Server Started on {self.host}:{self.port}")
        except Exception as e:
            print(f"[-] Server Creation Error:{e}")
        
        try:
            self.storage = StorageSolution(file)
            print(f"[-] Storage Instantiated on {self.storage.file.name}")
        except Exception as e:
            print(f"[-] Storage Creation Error:{e}")

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
            while self.servingStatus:
                match conn.recv(8):
                    case ReqType.STORE.value:
                        self.__modeStore(conn)
                    case ReqType.REQ_ALL.value:
                        self.__modeSendAll(conn)
                    case ReqType.REQ_NEW.value:
                        self.__modeSendNew(conn)
                    case ReqType.REQ_HASH.value:
                        self.__modeSendByHash(conn)
                    case ReqType.REQ_CONVO.value:
                        self.__modeSendConvo(conn)                   
                    case _:
                        print("[-] Invalid Request Type/ User Forcibly Terminated")
                        break

    def __modeStore(self, conn) -> None:
        print("[*] in store mode")
        conn.send(ReqType.ACK.value)
        print("[*] ACK sent to", conn.getpeername())
        data = deserializeMessage(conn.recv(2048))
        print("[*] Data received from", conn.getpeername())
        print(self.storage.storeMsg(data))
        return None

    def __modeSendAll(self, conn) -> None:
        print("[*] in send all mode")
        conn.send(ReqType.ACK.value)
        sleep(1)
        user = conn.recv(64).decode()

        print(f"[*] User: {user}, requested all messages")

        for msg in self.storage.getAllMsg(user):
            conn.sendall(serializeMessage(msg))
            sleep(0.1)
            
        conn.sendall(b"") # send empty string to indicate end of transmission
        return None
    
    def __modeSendNew(self, conn) -> None:
        print("[*] in send New mode")
        conn.send(ReqType.ACK.value)
        sleep(1)
        user = conn.recv(64).decode()
        print(f"[*] User: {user}, requested new messages")

        for msg in self.storage.getNewMsg(user):
            conn.sendall(serializeMessage(msg))
            sleep(0.1)
            
        conn.sendall(b"")
        return None
    
    def __modeSendConvo(self, conn) -> None:
        print("[*] In send convo mode")
        conn.send(ReqType.ACK.value)
        sleep(1)
        user = conn.recv(64).decode().split("|")
        print(f"[*] User: {user[0]}, requested conversation past with {user[1]}")

        for msg in self.storage.getConvo(user[0], user[1]):
            conn.sendall(serializeMessage(msg))
            sleep(0.1)
        
        conn.sendall(b"")
        return None

    def __modeSendByHash(self, conn) -> None:
        print("[*] in send all mode")
        conn.send(ReqType.ACK.value)
        sleep(2)
        return None
    
# Testing for this file
# if __name__ == "__main__":
#     server = Server("127.0.0.1", 8080, 1, Path.cwd())
#     server.startServing()