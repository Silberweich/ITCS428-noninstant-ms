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
    
    def sendMsg(self, msg: Message) -> bool:
        try:
            self.sock.send(ReqType.STORE.value)
            sleep(10)
            a = self.sock.recv(8)
            if a == ReqType.ACK.value:
                print(a)
            return True
        except Exception as e:
            print("[-] Message send Error", e)
            return False
    
    # retrieve all message designated for this client (self.username)
    def requestAllMsg(self):
        return None
    # retrieve new messages (Message.timesRequested == 0), this meant message is not read yet, designated for this client (self.username)
    def requestNewMsg(self):
        return None
    # retrieve message by hash designated for this client (self.username)
    def requestMsgByHash(self, hash: str):
        return None

# Testing for this file
if __name__ == "__main__":
    server = Client("jojo", socket.gethostname(), 8080)
    server.connect()
    server.sendMsg("test")
    sleep(5)