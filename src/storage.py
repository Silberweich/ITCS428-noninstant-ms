from message import Message

class StorageSolution():
    def __init__(self, path: str)-> None:
        self.path = path
        self.file = open(self.path, "a+")

    def store(self, msg: Message) -> bool:
        return True
    
    def getMsgByHash() -> Message:
        return "hash"
    
    def getMsgByHash() -> Message:
        return "hash"
    
    def getMsgByHash() -> Message:
        return "hash"