from src.message import Message, messageToJSON, messageFromJSON

from typing import List
from pathlib import Path

## @brief Class for creating StorageSolution object, direct interaction with file storage.
# @param host: host address of the server
# @param port: port of the server
# @param listen: number of connection to listen to simultaneously
# @param path: storage path, pass to StorageSolution
class StorageSolution():
    def __init__(self, path: Path)-> None:
        self.path = path / "store.txt"
        self.file = open(self.path, "a+")
        self.msgLine = []
        self.__loadMsgLine()

    def closeFileHandler(self, user:str) -> None:
        self.file.close()
    
    ## @brief private method, load every line of message from storage file
    # @param None
    # @details read every line of the storage file, and load it on self.msgLine
    # @return None
    def __loadMsgLine(self) -> None:
        self.file.seek(0)
        self.msgLine = [messageFromJSON(line.rstrip()) for line in self.file.readlines()]
        return None
    
    ## @brief private method, update data inside storage file
    # @param None
    # @details delete everything in the file, then rewrite with current self.msgLine, good update method
    # @return None
    def __updateAllMsg(self) -> None:
        self.file.seek(0)
        self.file.truncate()
        for msg in self.msgLine:
            self.file.write(messageToJSON(msg).rstrip() + "\n")
        self.file.flush()
        return None
    
    ## @brief store the new message to storage file
    # @param msg: The message to be appended to storage file
    # @details -
    # @return None
    def storeMsg(self, msg: Message) -> bool:
        print(f"[+] Storing message: {msg}")
        self.__loadMsgLine()
        self.msgLine.append(msg)
        self.__updateAllMsg()
        return True
    
    ## @brief get all message for a user
    # @param user: the username to get all message for 
    # @details get all message for user, and increment timesRequested, set firstRequested if it's 0
    # @return List of messages
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
    
    ## @brief get new (unread) message for a user
    # @param user: the username to get all message for
    # @details get new (unread) message for user, and increment timesRequested, set firstRequested if it's 0
    # @return List of messages
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
    
    ## @brief private method, update data inside storage file
    # @param user: 
    # @param partner:
    # @details 
    # @return List of messages
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


