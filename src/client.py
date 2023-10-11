from message import Message, createMessage, deserializeMessage, serializeMessage
from reqType import ReqType
from time import sleep
import pickle
import socket

## Client class
# @brief This class is used to create a client object connecting to server
class Client():
    def __init__(self, username: str, host: str, port: int) -> None:
        self.username = username
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def __repr__(self) -> str:
        return f"Client {self.username} Connected to: ({self.host}, {self.port})"

    def connect(self) -> bool:
        try:
            self.sock.connect((self.host, self.port))
            return True
        except Exception as e:
            print("[-] Connection Error", e)
            return False
    
    def disconnect(self) -> bool:
        try:
            self.sock.close()
            return True
        except Exception as e:
            print("[-] Disconnection Error", e)
            return False
        
    # send a message to server, server will store the message
    def sendMsg(self, msg: Message) -> bool:
        try:
            self.sock.send(ReqType.STORE.value)
            if self.sock.recv(8) == ReqType.ACK.value:
                print("[*] ACK received, start sending data...")
            return True
        except Exception as e:
            print("[-] Message send Error", e)
            return False
    
    # retrieve all message designated for this client (self.username)
    def requestAllMsg(self):
        try:
            self.sock.send(ReqType.STORE.value)
            if self.sock.recv(8) == ReqType.ACK.value:
                print("[*] ACK received, start sending data...")
                ## TODO: receive data one by one message
            return True
        except Exception as e:
            print("[-] Request All Error", e)
            return False
    
    # retrieve new messages (Message.timesRequested == 0), this meant message is not read yet, designated for this client (self.username)
    def requestNewMsg(self):
        try:
            self.sock.send(ReqType.STORE.value)
            if self.sock.recv(8) == ReqType.ACK.value:
                print("[*] ACK received, start sending data...")
                ## TODO: receive data one by one message
            return True
        except Exception as e:
            print("[-] Request New Error", e)
            return False
        
    # retrieve message by hash designated for this client (self.username)
    def requestMsgByHash(self, hash: str):
        return None

# Testing for this file
# if __name__ == "__main__":
#     server = Client("jojo", "127.0.0.1", 8080)
#     message = createMessage("jo", "mama", "hello mama mama hello lalalakll")
#     server.connect()
#     server.sendMsg(message)
#     sleep(5)