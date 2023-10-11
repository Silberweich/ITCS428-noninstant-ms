from enum import Enum

class ReqType(Enum):
    ACK = b"0"
    ERR = b"1"
    STORE = b"2"
    REQ_ALL = b"3"
    REQ_HASH = b"4"
    REQ_NEW = b"5"

# Testing for this file
if __name__ == "__main__":
    print(ReqType.ACK.value)