import socket
import argparse
import time
import os.path
import threading
import sys
from crypto import CryptoManager
from cipher import CaesarSalad

# Custom cryptography object -- using OpenSSL
cm = CryptoManager()

cs = CaesarSalad()

parser = argparse.ArgumentParser()

# Run in listen mode
parser.add_argument('-l', '--listen', dest='listen', action='store_true')

# IP address of the client to talk to
parser.add_argument('-i', '--ip', dest='dest_ip', action='store')

# Client's port
parser.add_argument('-p', '--port', type=int, dest='dest_port', action='store')

# Set listen mode off by default
parser.set_defaults(listen=False)

# Parse arguments
args = parser.parse_args()

# Pull ip and port from args
dest_ip = args.dest_ip
dest_port = args.dest_port

print("!!! [CAESAR SALAD] !!!")

alias = input("Enter a display name: ")

connection_status = True


def receive_in_bg(sock, user):
    while connection_status:
        try:
            if sock:
                data = sock.recv(1024)
                if data is None:
                    break
                print("\n" + user + ": " + cs.cs_decode(bytes(data).decode()))
                print(alias + " >> ", end="", flush=True)
            else:
                break
        except:
            break

if args.listen:
    print("\n[CAESAR] Running in listen mode...")
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # In this case, using "dest_port" as the port to listen on instead
    conn.bind(('localhost', dest_port))
    print("[CAESAR] Listening on port " + str(dest_port))
    conn.listen(1)
    conn, addr = conn.accept()

    # Handle initial handshake (listening side)
    # My thinking is to do it before initializing the background thread
    # Reason: background thread is told to print out messages it receives--not use for handshake

    other_username = conn.recv(1024).decode()
    conn.send(bytes(alias, 'utf-8'))

    print("\n[CAESAR] Establishing handshake with: " + other_username)

    # receive shared base
    shared_base = conn.recv(1024)
    shared_base_f = open("keys/dhp.pem", "w")
    shared_base_f.write("-----BEGIN DH PARAMETERS-----\n"+shared_base.decode()+"\n-----END DH PARAMETERS-----\n")
    shared_base_f.close()

    while True:
        if shared_base_f.closed:
            break

    cm.generate_private_key()
    cm.generate_public_key()

    # receive peer's pub key
    peerkey = conn.recv(1024)
    peerkey_f = open("keys/peer.pem", "w")
    peerkey_f.write("-----BEGIN PUBLIC KEY-----\n"+peerkey.decode()+"\n-----END PUBLIC KEY-----\n")
    peerkey_f.close()

    # send this client's pub key
    my_pub_key = cm.read_key(type_file=CryptoManager.PUBLIC_KEY)
    conn.send(bytes(my_pub_key, "utf-8"))

    cm.derive_shared_secret()

    listenThread = threading.Thread(target=receive_in_bg, args=[conn, other_username])
    listenThread.start()

    message = input(alias + " >> ")
    #message = input()
    while message != 'q':
        if message != '':
            encoded_message = cs.cs_encode(message)
            conn.send(bytes(encoded_message, "utf-8"))
        message = input(alias + " >> ")
        #message = input()
        #time.sleep(0.2)
    print("[CAESAR] Connection closed...")
    connection_status = False
    listenThread.join()
    conn.close()
    sys.exit()
else:
    print("\n[CAESAR] Establishing connection...")
    # Set up socket connection
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((dest_ip, dest_port))

    # Handle initial handshake
    conn.send(bytes(alias, 'utf-8'))
    other_username = conn.recv(1024).decode()

    print("\n[CAESAR] Establishing handshake with: " + other_username)

    cm.generate_shared_base()
    cm.generate_private_key()
    cm.generate_public_key()

    shared_base = cm.read_key(type_file=CryptoManager.SHARED_BASE)
    conn.send(bytes(shared_base, "utf-8"))

    public_key = cm.read_key(type_file=CryptoManager.PUBLIC_KEY)
    conn.send(bytes(public_key, "utf-8"))

    # receive peer's pub key
    peerkey = conn.recv(1024)
    peerkey_f = open("keys/peer.pem", "w")
    peerkey_f.write("-----BEGIN PUBLIC KEY-----\n"+peerkey.decode()+"\n-----END PUBLIC KEY-----\n")
    peerkey_f.close()

    cm.derive_shared_secret()

    listenThread = threading.Thread(target=receive_in_bg, args=[conn, other_username])
    listenThread.start()

    message = input(alias + " >> ")
    #message = input()
    while message != 'q':
        if message != '':
            encoded_message = cs.cs_encode(message)
            conn.send(bytes(encoded_message, "utf-8"))
        message = input(alias + " >> ")
        #message = input()
        #time.sleep(0.2)
    print("[CAESAR] Connection closed...")
    connection_status = False
    listenThread.join()
    conn.close()
    sys.exit()
