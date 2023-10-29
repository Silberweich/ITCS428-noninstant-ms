from src.client import Client
from src.server import Server
from src.message import createMessage
from pathlib import Path
import datetime
import argparse

## Every CLI component will be written in this file

prompt = "\nWhat do you want to do? \n(1. sendmessage, 2. get all message, 3. get new (unread) messagges, 4. get convo, 5. exit): \n>"
prettyprint = "\n[>] From: {u} -> {t} \n[>] Time: {s} \n[>] Message: {m}"
convoprint = "\n[{x}] From: {u} -> {t} \n[{x}] Time: {s}{r} \n[{x}] Message: {m}"

both_mode = lambda s, c: not (s and c)

parser = argparse.ArgumentParser(
    prog = "non-instant messenger app",
    description= 'Computationally inefficient, error prone, badly implemented, non-instant messenger app with no security whatsoever',
    epilog = "6388002 Phuthana Ampunant, 6388035 Phichayut Ngoennim | ITCS428 Term project submission 1"
    )

parser.add_argument("-s", "--server", help="run this program as server mode", action="store_true")
parser.add_argument("-c", "--client", help="run this program as client mode", action="store_true")
parser.add_argument("-a", "--address", help="either bind server to this address or connect client to this address (default 127.0.0.1)", type=str, default=r"127.0.0.1")
parser.add_argument("-p", "--port", help="either bind server to this port or connect client to this port (default 8080)", type=int, default=8080)

args = parser.parse_args()

def main() -> None:
    if not both_mode(args.server, args.client):
        print("[X] please pick one of the option (-s, -c), not both, EXITING")
        exit()

    if not args.server and not args.client:
        print(f"runnning server on {args.address}:{args.port}" )
        serverMode()  
    elif args.client:
        print(f"runnning client connecting to {args.address}:{args.port}")
        clientMode()
    else:
        print(f"runnning server on {args.address}:{args.port}")
        serverMode()
        

def serverMode() -> None:
    print("Server is starting and cannot be interrupted with Ctrl+C ┻━┻ ︵ヽ(`Д´)ﾉ︵ ┻━┻")
    server = Server(args.address, args.port, 2, Path.cwd())
    server.startServing()

def clientMode() -> None:
    user = input("Enter your username: ")
    print("Initializing Client...")
    client = Client(user, args.address, args.port)
    client.connect()

    while True:
        match int(input(prompt).lower().strip()):
            case 1:
                toUser = input("Enter recipient username: ")
                msg = input("Enter message: ")
                client.sendMsg(createMessage(user, toUser, msg))
            case 2:
                [print(prettyprint.format(u = i.fromUsr,
                                          t = i.toUsr, 
                                          s = datetime.datetime.fromtimestamp(i.timeStamp), 
                                          m = i.msgData)) 
                                        for i in client.requestAllMsg()]
            case 3:
                [print(prettyprint.format(u = i.fromUsr,
                                          t = i.toUsr, 
                                          s = datetime.datetime.fromtimestamp(i.timeStamp), 
                                          m = i.msgData)) 
                                        for i in client.requestNewMsg()] 
            case 4:
                partner = input("who is the conversation partner:")
                client.requestConvo(partner)
                [print(convoprint.format (x = ">" if i.fromUsr == user else "<",
                                          u = i.fromUsr,
                                          t = i.toUsr,
                                          s = datetime.datetime.fromtimestamp(i.timeStamp),
                                          r = f"| READ On: {datetime.datetime.fromtimestamp(i.firstRequested)}" if i.fromUsr == user else "",
                                          m = i.msgData))
                                        for i in client.requestConvo(partner)]
            case 5: 
                client.disconnect()
                exit()
            case _:
                print("Invalid input, please try again")
                continue

main()