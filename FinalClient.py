"""
Author: Luka Moon
Class: CSI-275-01
Assignment: Final

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given
fully-documented references to the work of others. I understand the definition
and consequences of plagiarism and acknowledge that the assessor of this
assignment may, for the purpose of assessing this assignment:
- Reproduce this assignment and provide a copy to another member of academic
- staff; and/or Communicate a copy of this assignment to a plagiarism checking
- service (which may then retain a copy of this assignment on its database for
- the purpose of future plagiarism checking)"""
import socket, json, sys
from threading import Thread
HOST = 'localhost'
PORT = 8080

"""get user info"""
def on_start():
    global username
    done = ""

    while done != "done":
        user_input = input("enter username to be known as in chat room: \n")
        done = input("type done to confirm, enter to change name: \n ")

        if not user_input.isalnum():
            print("username must be alphanumeric")
    username = user_input
    print("username is: " + username)

"""handle sending of data, format it according to the command the user picks"""
def send_thread(sock):
    while True:
        try:

            msg = input("enter message to send with a given command: \n")
            if not msg.startswith("/"):
                print("error, make sure to include a supported command before the message!"
                      " /help to see them")

            elif msg.startswith("/help"):
                print("/exit to leave chatroom, /dm to send a private message, "
                      "/bc to broadcast to everyone in the chatroom")

            elif msg.startswith("/exit"):
                print("exiting")
                sock.close()
                sys.exit(1)
                break

            elif msg.startswith("/update"):
                print("updating chats")


            elif msg.startswith("/dm"):
                msg_split = msg.split(" ",2)
                target = msg_split[1]
                msg_to_send = msg_split[2]

                msg_json = {
                    "cmd": "dm",
                    "user": username,
                    "target": target,
                    "msg": msg_to_send
                }

            elif msg.startswith("/bc"):
                msg_json = {
                    "cmd": "bc",
                    "user": username,
                    "msg": msg
                }
            else:
                print("unknown command type /help")
                continue

            msg_json = json.dumps(msg_json).encode("utf-8")
            jsonlen = len(msg_json)
            sock.send(jsonlen.to_bytes(4, byteorder='big'))
            sock.send(msg_json)
        except Exception as e:
            print(e)
            print("error sending message")
            break

"""send the start message to the server, print messages sent"""
def recv_thread(sock):
    startmsg = {
        "cmd": "START",
        "user": username
    }
    msg_in_bytes = json.dumps(startmsg).encode('utf-8')
    sock.send(len(msg_in_bytes).to_bytes(4, "big"))
    sock.send(msg_in_bytes)

    while True:
        try:
            data = sock.recv(4)
            if not data:
                print("idk connection failed")
                break

            msg_len = int.from_bytes(data, "big")
            msg_bytes = recvall(sock, msg_len)
            msg_decoded = msg_bytes.decode('utf-8')
            msg_json = json.loads(msg_decoded)
            print(msg_json['user'], msg_json['msg'])

        except Exception as e:
            print(e)
            print("error receiving message")
"""open two sockets and related threads"""
def network():
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_sock.connect((HOST, 8080))

    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recv_sock.connect((HOST, 8081))
    print("connected")

    Thread(target=send_thread, args=(send_sock,)).start()
    Thread(target=recv_thread, args=(recv_sock,)).start()

"""taken from one of our labs, recieves the rest of a message"""
def recvall(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received'
                           ' %d bytes before the socket closed'
                           % (length, len(data)))
        data += more
    return data


def main():
    on_start()

if __name__ == "__main__":
    main()
    network()
