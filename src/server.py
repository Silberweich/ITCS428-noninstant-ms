from src.message import deserializeMessage, serializeMessage
from src.storage import StorageSolution
from src.reqType import ReqType

from time import sleep
from pathlib import Path
import threading
import socket

## @brief Class for creating server object, and serving client
# @param host: host address of the server
# @param port: port of the server
# @param listen: number of connection to listen to simultaneously
# @param path: storage path, pass to StorageSolution
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
    
    ## @brief start serving, pick modes according to request type sent by client
    #  @param None
    #  @details loop forever, accept connection, spawn thread to handle connection (phase 2)
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
    
    ## @brief private method, handle storage of data sent by client
    # @param conn: connection object from startServing()
    # @details After startServing() receive ReqType.STORE, it will enter this mode which calls self.storage to store the message
    # @return None
    def __modeStore(self, conn) -> None:
        print("[*] in store mode")
        conn.send(ReqType.ACK.value)
        print("[*] ACK sent to", conn.getpeername())
        data = deserializeMessage(conn.recv(2048))
        print("[*] Data received from", conn.getpeername())
        print(self.storage.storeMsg(data))
        return None

    ## @brief private method, handle sending all message to client
    # @param conn: connection object from startServing()
    # @details After startServing() receive ReqType.REQ_ALL, it will enter this mode which calls self.storage to get all messages
    # @return None
    def __modeSendAll(self, conn) -> None:
        print("[*] in send all mode")
        conn.send(ReqType.ACK.value)
        sleep(1)
        user = conn.recv(64).decode()

        print(f"[*] User: {user}, requested all messages")

        for msg in self.storage.getAllMsg(user):
            conn.sendall(serializeMessage(msg))
            sleep(0.1)
            
        conn.sendall(b"")
        return None
    
    ## @brief private method, handle sending unread/new message to client
    # @param conn: connection object from startServing()
    # @details After startServing() receive ReqType.REQ_NEW, it will enter this mode which calls self.storage to get new messages
    # @return None
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
    
    ## @brief private method, handle sending list message between two user (client, partner) to the requesting client
    # @param conn: connection object from startServing()
    # @details After startServing() receive ReqType.REQ_CONVO, it will enter this mode which calls self.storage to message between two users.
    # @return None
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
    
