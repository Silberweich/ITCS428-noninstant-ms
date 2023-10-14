from src.message import Message, messageToJSON, messageFromJSON, createMessage, msgPrint

from typing import List
from pathlib import Path

## Extremely inefficient storage solution, 
#  read everything from file to mem, update mem, then write mem to file on every operation haha
class StorageSolution():
    def __init__(self, path: Path)-> None:
        self.path = path / "store.txt"
        self.file = open(self.path, "a+")
        self.msgLine = []
        self.__loadMsgLine()
        print(f"[+] DB: {self.msgLine}")

    def closeFileHandler(self, user:str) -> None:
        self.file.close()

    def storeMsg(self, msg: Message) -> bool:
        print(f"[+] Storing message: {msg}")
        self.__loadMsgLine()
        self.msgLine.append(msg)
        self.__updateAllMsg()
        return True
    
    def __loadMsgLine(self) -> None:
        self.file.seek(0)
        self.msgLine = [messageFromJSON(line.rstrip()) for line in self.file.readlines()]
        return None
    
    def __updateAllMsg(self) -> None:
        self.file.seek(0)
        self.file.truncate()
        for msg in self.msgLine:
            self.file.write(messageToJSON(msg).rstrip() + "\n")
        self.file.flush()
        return None

    def getMsgByHash(self, user:str, hash:str) -> Message:
        self.__loadMsgLine()
        for msg in self.msgLine:
            if msg.toUsr == user and msg.msgHash == hash:
                msg.incRequested()
                self.__updateAllMsg()
                return msg
        return None
    
    def getNewMsg(self, user:str) -> List[Message]:
        self.__loadMsgLine()
        messages = []
        for msg in self.msgLine:
            if msg.toUsr == user and msg.timesRequested == 0:
                messages.append(msg)
                msg.incRequested()
                if msg.firstRequested == 0: msg.setFirstRequested()
        self.__updateAllMsg()
        return messages
    
    def getAllMsg(self, user:str) -> List[Message]:
        self.__loadMsgLine()
        messages = []
        for msg in self.msgLine:
            if msg.toUsr == user:
                messages.append(msg)
                msg.incRequested()
                if msg.firstRequested == 0: msg.setFirstRequested()
        self.__updateAllMsg()
        return messages
    
    def getConvo(self, user:str, partner:str) -> List[Message]:
        self.__loadMsgLine()
        messages = []
        for msg in self.msgLine:
            if (msg.toUsr == user and msg.fromUsr == partner) or (msg.toUsr == partner and msg.fromUsr == user):
                messages.append(msg)
                msg.incRequested()
                if msg.firstRequested == 0: msg.setFirstRequested()
        self.__updateAllMsg()
        return messages

#  if __name__ == "__main__":
    # store = StorageSolution(Path.cwd())
    
    # print(store.msgLine)
    # # print("\n\n>", store.getNewMsg("testrecv"))
    # print("\n\n>", store.getAllMsg("testrecv"))
    # print("\n\n>", store.getMsgByHash("to","fe7f20fc7974ef4b8aa9727966133ba5"))
