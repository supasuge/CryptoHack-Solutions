from pwn import *
import time
from Crypto.Util.number import long_to_bytes
import hashlib
import json

# Connect to the server
HOST = "socket.cryptohack.org"
PORT = 13372

def generate_key(timestamp):
    key = long_to_bytes(timestamp)
    return hashlib.sha256(key).digest()

def decrypt_flag(encrypted_flag, key):
    encrypted_flag = bytes.fromhex(encrypted_flag)
    return bytes([encrypted_flag[i] ^ key[i] for i in range(len(encrypted_flag))])

def main():
    # Synchronize time with the server
    r = remote(HOST, PORT)
    
    # Read the initial message ("Gotta go fast!")
    r.recvline()

    # Request the encrypted flag
    r.sendline(b'{"option": "get_flag"}')
    response = r.recvline().decode()
    
    # Parse JSON response
    response_json = json.loads(response)
    encrypted_flag = response_json["encrypted_flag"]
    
    # Calculate the key based on approximate timestamp
    server_time = int(time.time())
    for offset in range(-5, 6):  # Adjust offset range for synchronization error
        timestamp = server_time + offset
        key = generate_key(timestamp)
        try:
            decrypted_flag = decrypt_flag(encrypted_flag, key)
            if b"crypto{" in decrypted_flag:
                print(f"Decrypted flag: {decrypted_flag.decode()}")
                break
        except Exception:
            continue

    r.close()

if __name__ == "__main__":
    main()

