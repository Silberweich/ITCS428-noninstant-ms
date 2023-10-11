from dataclasses import dataclass
from hashlib import md5
import datetime


## Message class
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
    timeStamp: datetime.datetime = datetime.datetime.now()

## createMessage
# @brief This function is used to create a message object
def createMessage(fromUsr: str, toUsr: str, msgData:str) -> Message:
    return Message(
        md5((msgData + str(datetime.datetime.now())).encode()), 
        fromUsr, 
        toUsr, 
        msgData
        )

# Testing for this file
# if __name__ == "__main__":
#     message = createMessage("jo", "mama", "hello mama")
#     print(datetime.datetime.now())
#     print(message)