# ITCS428: Non-instant Messaging System (Term project)

## User guide
To start a server:
```
$ python cli_main.py -s
```
To start a CLI client:
```
$ python cli_main.py -c
```
To start a CLI Help!!!:
```
$ python cli_main.py --help
```
To start GUI application:
```
$ python gui_main.py
```

## Submission Requirements
-	[x] For network side, only low level ***socket*** API is allowed, no urllib, smtp or other application level modules. Work as group of 1-2 people.
- [x] **25 September 2023**: group member + mockup design
- [x] **15 October 2023** [V1]: Single connection, CLI milestone
- [x] **25 October 2023** [V2]: Select a multi-connection method
  - [x] use **Treading**
  - [ ] use **Multi-Process**

### Project Requirements
-	Message destined to a receiver must be stored on the server in form of a file. 
-	The receiver will send a command to look at messages destined to him/her.
-	The server must provide information about what time the message has sent.
-	The sender can know what time the message has been read.
-	Students may add more functions that you think necessary or cool!

### Functional Requirement (initial)
- The software will take argument, server or client, then start respective mode.
- No security, user can request any message as long as they know the username
- ***Server***:
  - Server run constantly, waiting for TCP connection on (IP, port)
    - server send(by client request) or receive message
    - once there is a request, server reads a JSON file for all matching `to`. Then send those data. Find a way to clear all the memory afterward?
- ***Client***:
  - Client will not store any persistent data
  - Start as client, can do 2 things
    - **Send** message to server, the message is designated to another user.
    - **Request** message from server as {username}. 
    - message data processing is done at client, then send to server as bytes.
- ***message format***
  - The message can be requested for view by receiver or sender
  - local storage of the data for server will be done as JSON.
  - ```python
    # this should be a dataclass?
    message {
        "hash": {md5 hash digest of the message},
        "from": "from user",
        "to": "destination user",
        "time": datetime.datetime.now()
        "message": "Long message string"
    }
    ```
### You can
- impersonate other people username, because there is no password
- wait for message to load the more message you have, problem with syncing sending multiple packet, despite the fact that all packet is sent successfully (wireshark), the later packet is not properly received and ACK. Stupid.
