#!/usr/bin/env python3

import hashlib
import string
import socket
import time
import sys

def crack_pw(passwords, characters, hash_str):
    for c in characters:
        for p in passwords:
            # crack hashes
            test_hash = hashlib.sha256((c + p).encode('utf_8')).hexdigest()
            
            if test_hash == hash_str:
                return c + p

    return None

def server_crack():

    with open('passwords.txt', 'r') as password_file:
        passwords = password_file.read().splitlines() # open and read passwords.txt

    characters = string.ascii_lowercase
    server_ip = '134.209.128.58'
    server_port = 1337

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_ip, server_port))

    msg_lengths = [26, 22, 16]

    # parse data
    # crack 3 times
    for i in range(1,4):
        time.sleep(0.1)
        # consume server message
        q = s.recv(msg_lengths[i - 1])
        hash_str = s.recv(64).decode('utf_8')

        # consume prompt
        q = s.recv(5)

        pw = crack_pw(passwords, characters, hash_str)

        if pw:
            # send cracked input to server
            s.send(pw.encode('utf_8'))
            s.send('\n'.encode('utf_8'))

        else:
            print('Failed to crack hash' + hash_str, file=sys.stderr)
            sys.exit(-1)

    print(s.recv(1024).decode('utf_8'))

if __name__ == "__main__":
    server_crack()
