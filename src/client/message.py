from dataclasses import dataclass
from hashlib import md5
import datetime
import pickle

## Message dataclass
#  @brief This dataclass is for message objects
#  @param msgHash The hash of the messageData
#  @param fromUsr The username of the sender 
#  @param toUsr The username of the recipient
#  @param timeStamp The time the message was sent (generate when dataclass is instantiated)
@dataclass
class Message:
    msgHash: str
    fromUsr: str
    toUsr: str
    msgData: str
    timesRequested: int = 0
    timeStamp: datetime.datetime = datetime.datetime.now()

## createMessage
# @brief This function is used to create a message object
def createMessage(fromUsr: str, toUsr: str, msgData:str) -> Message:
    return Message(
        md5((msgData + str(datetime.datetime.now())).encode()).hexdigest(), 
        fromUsr, 
        toUsr, 
        msgData
        )
## message printing
def msgPrint(msg: Message):
    print(f"From: {msg.fromUsr}\nTime: {msg.timeStamp}\nMessage: {msg.msgData}\n")
    return True

## serializeMessage and deserializeMessage
#  These functions are used to serialize and deserialize messages to and from bytes, for data transfer
def serializeMessage(msg: Message) -> bytes:
    return pickle.dumps(msg)

def deserializeMessage(msg: bytes) -> Message:
    return pickle.loads(msg)

# Testing for this file
if __name__ == "__main__":
    message = createMessage("jo", "mama", "hello mama")
    print(datetime.datetime.now())
    semsg = serializeMessage(message)
    print(">>", semsg)
    msg = deserializeMessage(semsg)
    print(">>", msg)
    print(msg.timeStamp.strftime("%H:%M:%S"))
    msgPrint(msg)