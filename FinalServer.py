import socket, json
from threading import Thread
clients = []
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
HOST = 'localhost'
READ_PORT = 8080
WRITE_PORT = 8081
"""creates a new thread for every connection recieved"""
def read_thread(serv_sock):
    while True:
        client, addr = serv_sock.accept()
        print("reader, new client connected", addr)
        Thread(target=handle_client, args=(client,)).start()

"""helper for read thread that handles all the commands and data it recieves"""
def handle_client(client_sock):
    while True:
        try:
            msglength = client_sock.recv(4)
            if not msglength:
                print("client disconnected")


            msgnum = int.from_bytes(msglength, byteorder='big')
            msg_real = recvall(client_sock, msgnum)
            msg_real_decoded = json.loads(msg_real.decode('utf-8'))
            print("msg: ", msg_real_decoded)

            cmd = msg_real_decoded.get('cmd')

            if cmd == "exit":
                user = msg_real_decoded.get('user')
                for sock, name in clients:
                    if name == user:
                        print(f"{name} left")
                        clients.remove((sock, name))
                        sock.close()
                        break
                break

            elif cmd == "bc":
                for client, _ in clients:
                    try:
                        response = msg_real_decoded
                        response_json = json.dumps(response).encode('utf-8')
                        response_len = len(response_json).to_bytes(4, byteorder='big')
                        client.send(response_len)
                        client.send(response_json)
                    except Exception as e:
                        print("uhh", e)

            elif cmd == "dm":
                    try:
                        response = msg_real_decoded
                        response_json = json.dumps(response).encode('utf-8')
                        response_len = len(response_json).to_bytes(4, byteorder='big')

                        target = msg_real_decoded['target']
                        for client, name in clients:
                            if name == target:
                                client.send(response_len)
                                client.send(response_json)

                    except Exception as e:
                        print("uhh", e)

        except Exception as e:
            print("read_thread", e)
            break
    client_sock.close()

"""appends client data to a list on connection for later usage"""
def write_thread(serv_sock):
    while True:
        client, addr = serv_sock.accept()
        print("writer, new client connected", addr)
        try:
            msglength = client.recv(4)

            msgnum = int.from_bytes(msglength, byteorder='big')
            msg_real = recvall(client, msgnum)
            msg_real_decoded = json.loads(msg_real.decode('utf-8'))

            if msg_real_decoded['cmd'] == "START":
                user = msg_real_decoded.get('user')
                clients.append((client, user))

        except Exception as e:
            print("write_thread ", e)

"""create and bind a reading and writing socket and related threads"""
def network():
    read_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    write_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    read_sock.bind((HOST, READ_PORT))
    read_sock.listen(5)

    write_sock.bind((HOST, WRITE_PORT))
    write_sock.listen(5)

    Thread(target=read_thread, args=(read_sock,)).start()
    Thread(target=write_thread, args=(write_sock,)).start()

"""taken from one of our labs, gets the rest of a messages data"""
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

if __name__ == "__main__":
    network()
