#!/usr/bin/env python3

import hashlib
import string

def crack():
    with open('hashes.txt', 'r') as hash_file:
        hashes = hash_file.read().splitlines() # open and read hashes.txt

    with open('passwords.txt', 'r') as password_file:
        passwords = password_file.read().splitlines() # open and read passwords.txt

    characters = string.ascii_lowercase

    for c in characters:
        for p in passwords:
            # crack hashes
            test_hash = hashlib.sha256((c + p).encode('utf-8')).hexdigest()

            if test_hash in hashes:
                # print hashes as 'input:hash'
                # i.e.  yeet:909104cdb5b06af2606ed4a197b07d09d5ef9a4aad97780c2fe48053bce2be52
                print(c + p + ':' + test_hash)

if __name__ == "__main__":
    crack()
