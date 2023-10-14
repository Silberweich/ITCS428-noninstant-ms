from src.message import Message, createMessage, deserializeMessage, serializeMessage
from src.reqType import ReqType
from time import sleep
from typing import List
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
        self.sock.settimeout(3)
    
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
                self.sock.send(serializeMessage(msg))
            return True
        except Exception as e:
            print("[-] Message send Error", e)
            return False
    
    # retrieve all message designated for this client (self.username)
    def requestAllMsg(self) -> List[Message]:
        messages = []
        try:
            self.sock.send(ReqType.REQ_ALL.value)
            if self.sock.recv(8) != ReqType.ACK.value: 
                raise Exception("REQ_ALL ACK not received")
            print("[*] REQ_ALL ACK received, start receiving data process...")
            self.sock.send(self.username.encode())
            while True:
                sleep(0.5)
                print("[*] recving")
                data = self.sock.recv(4096)
                
                if not data or data == b"": break
                messages.append(deserializeMessage(data))
            print("[*] All data received")
            return messages
        
        except Exception as e:
            if e == socket.timeout:
                print("[+] Finished Receiving")
            print("[-] Request All Error", e, "Or probably receive all, error handling is hard")
            return messages
    
    # retrieve new messages (Message.timesRequested == 0), this meant message is not read yet, designated for this client (self.username)
    def requestNewMsg(self) -> List[Message]:
        messages = []
        try:
            self.sock.send(ReqType.REQ_NEW.value)
            if self.sock.recv(8) != ReqType.ACK.value: 
                raise Exception("REQ_ALL ACK not received")
            print("[*] REQ_NEW ACK received, start receiving data process...")
            self.sock.send(self.username.encode())
            while True:
                sleep(0.5)
                print("[*] recving")
                data = self.sock.recv(4096)
                
                if not data or data == b"": break
                messages.append(deserializeMessage(data))
            print("[*] All data received")
            return messages
        
        except Exception as e:
            if e == socket.timeout:
                print("[+] Finished Receiving")
            print("[-] Request All Error", e, "Or probably receive all, error handling is hard")
            return messages
        
    # retrieve message by hash designated for this client (self.username)
    def requestMsgByHash(self, hash: str):
        return None

# Testing for this file
# if __name__ == "__main__":
#     server = Client("mama", "127.0.0.1", 8080)
#     message = createMessage("mama", "jo", "hello jojo jojo")
#     server.connect()
#     sleep(1)
#     print(server.requestAllMsg())
#     server.disconnect()