from enum import Enum

class ReqType(Enum):
    ACK = b"0"
    ERR = b"1"
    STORE = b"2"
    REQ_ALL = b"3"
    REQ_NEW = b"4"
    REQ_HASH = b"5"
    REQ_USER = b"6"
    FIN = b"8"

# Testing for this file
if __name__ == "__main__":
    print(ReqType.ACK.value)