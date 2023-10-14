from message import Message, messageToJSON, messageFromJSON, createMessage, msgPrint

from typing import List
from pathlib import Path

class StorageSolution():
    def __init__(self, path: Path)-> None:
        self.path = path / "store.txt"
        self.file = open(self.path, "a+")
        self.msgLine = []

    def closeFileHandler(self, user:str) -> None:
        self.file.close()

    def storeMsg(self, msg: Message) -> bool:
        self.file.write(messageToJSON(msg))
        return True
    
    def loadMsgLine(self) -> None:
        print(self.file.read())
        # for line in self.file.read():
        #     print(">", line)
        # self.msgLine = [messageFromJSON(line.rstrip()) for line in self.file.readlines()]
        return None

    def getMsgByHash(self, user:str, hash:str) -> Message:
        return "hash"
    
    def getNewMsg(self, user:str) -> List[Message]:
        return "hash"
    
    def getAllMsg(self, user:str) -> List[Message]:
        return "hash"
    
if __name__ == "__main__":
    store = StorageSolution(Path.cwd())
    print("test")
    msg = createMessage("from", "to", "datadatadatadatadata")
    store.storeMsg(msg)
    msg = createMessage("test", "testrecv", "better answer my message soon")
    store.storeMsg(msg)
    msg = createMessage("test", "testrecv", "Ey yo, answer my message")
    store.storeMsg(msg)
    msg = createMessage("from", "to", "dqaaaaaa")
    store.storeMsg(msg)
    msg = createMessage("from", "to", "dataddsdsddsdsd")
    store.storeMsg(msg)
    store.loadMsgLine()
    print(store.msgLine)
