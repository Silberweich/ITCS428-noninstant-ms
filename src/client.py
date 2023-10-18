from src.message import Message, deserializeMessage, serializeMessage
from src.reqType import ReqType
from time import sleep
from typing import List
import socket

## @brief Class for creating client object
# @param username: username of the client in this instance
# @param host: host address of the server
# @param port: port of the server
class Client():
    def __init__(self, username: str, host: str, port: int) -> None:
        self.username = username
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(3)
    
    def __repr__(self) -> str:
        return f"Client {self.username} Connected to: ({self.host}, {self.port})"
    
    ## @brief Open socket, connect to server
    def connect(self) -> bool:
        try:
            self.sock.connect((self.host, self.port))
            return True
        except Exception as e:
            print("[-] Connection Error", e)
            return False
    
    ## @brief close socket
    def disconnect(self) -> bool:
        try:
            self.sock.close()
            return True
        except Exception as e:
            print("[-] Disconnection Error", e)
            return False
        
    ## @brief send message to server
    # @param msg: message to be sent
    # @details send two packet, first packet is the request type, second packet is the message
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
    
    ## @brief request every messages designated towards self.username
    # @param None
    # @details send REQ_ALL to set server mode, wait ACK, send username, wait for data
    # @return List[Message] list of messages
    def requestAllMsg(self) -> List[Message]:
        messages = []
        try:
            self.sock.send(ReqType.REQ_ALL.value)
            if self.sock.recv(8) != ReqType.ACK.value: 
                raise Exception("REQ_ALL ACK not received")
            print("[*] REQ_ALL ACK received, start receiving data process...")
            self.sock.send(self.username.encode())
            while True:
                sleep(0.1)
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
    
    ## @brief request every un-read messages designated towards self.username
    # @param None
    # @details send REQ_NEW to set server mode, wait ACK, send username, wait for data
    # @return List[Message] list of messages that has not been requested before
    def requestNewMsg(self) -> List[Message]:
        messages = []
        try:
            self.sock.send(ReqType.REQ_NEW.value)
            if self.sock.recv(8) != ReqType.ACK.value: 
                raise Exception("REQ_ALL ACK not received")
            print("[*] REQ_NEW ACK received, start receiving data process...")
            self.sock.send(self.username.encode())
            while True:
                sleep(0.1)
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
    
    ## @brief request conversation between self.username and partner (which is their conversation partner username)
    # @param partner: conversation partner username
    # @details send REQ_CONVO to set server mode, wait ACK, send username + partnername, wait for data
    # @return List[Message] list of messages in the conversation
    def requestConvo(self, partner: str) -> List[Message]:
        messages = []
        try:
            self.sock.send(ReqType.REQ_CONVO.value)
            if self.sock.recv(8) != ReqType.ACK.value: 
                raise Exception("REQ_ALL ACK not received")
            print("[*] REQ_CONVO ACK received, start receiving data process...")
            self.sock.send((self.username + "|" + partner).encode())
            while True:
                sleep(0.1)
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

