from dataclasses import dataclass
from hashlib import md5
import time
import pickle
import json

## @brief Message dataclass, used to store message data
@dataclass
class Message:
    msgHash: str
    fromUsr: str
    toUsr: str
    msgData: str
    timesRequested: int = 0
    firstRequested: float = 0
    timeStamp: float = time.time()

    def incRequested(self):
        self.timesRequested += 1
        return True
    
    def setFirstRequested(self):
        self.firstRequested = time.time()
        return True

def createMessage(fromUsr: str, toUsr: str, msgData:str) -> Message:
    return Message(
        md5((msgData + str(time.time())).encode()).hexdigest(), 
        fromUsr, 
        toUsr, 
        msgData
        )

def messageToJSON(msg: Message) -> str:
    return json.dumps(msg.__dict__)

def messageFromJSON(jsonMsg: str) -> Message:
    return Message(**json.loads(jsonMsg))

def serializeMessage(msg: Message) -> bytes:
    return pickle.dumps(msg)

def deserializeMessage(msg: bytes) -> Message:
    return pickle.loads(msg)
