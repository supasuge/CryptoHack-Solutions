import requests

from Crypto.Util.Padding import unpad


def encrypt_flag(key):

    res = requests.get(f"http://aes.cryptohack.org/triple_des/encrypt_flag/{key.hex()}")

    return bytes.fromhex(res.json()['ciphertext'])


def encrypt(key, plaintext):

    res = requests.get(f"http://aes.cryptohack.org/triple_des/encrypt/{key.hex()}/{plaintext.hex()}/")

    return bytes.fromhex(res.json()['ciphertext'])


# DES weak keys

key1 = b"\x01\x01\x01\x01\x01\x01\x01\x01"

key2 = b"\xfe\xfe\xfe\xfe\xfe\xfe\xfe\xfe"


# 3DES weak key = key1 || key2

key = key1 + key2


encrypted_flag = encrypt_flag(key)

flag = unpad(encrypt(key, encrypted_flag), 8)

print(flag.decode())
