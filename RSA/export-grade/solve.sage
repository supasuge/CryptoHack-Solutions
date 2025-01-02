from sage.groups.generic import discrete_log

from sage.arith.misc import power_mod

from Crypto.Cipher import AES

from Crypto.Util.Padding import pad, unpad

import hashlib


def is_pkcs7_padded(message):

    padding = message[-message[-1]:]

    return all(padding[i] == len(padding) for i in range(0, len(padding)))



def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):

    # Derive AES key from shared secret

    sha1 = hashlib.sha1()

    sha1.update(str(shared_secret).encode())

    key = sha1.digest()[:16]

    # Decrypt flag

    ciphertext = bytes.fromhex(ciphertext)

    iv = bytes.fromhex(iv)

    cipher = AES.new(key, AES.MODE_CBC, iv)

    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):

        return unpad(plaintext, 16).decode()

    else:

        return plaintext.decode()


p = 16007670376277647657
g = Mod(2, p)
A = Mod(153868131804831070, p)
B = 445893396720574298
iv = "502b389f5b3658b3672ed9c8e0466c83"
encrypted_flag = "4e47d4232fab3dca7ee1f830f049a491be2af0b1a18fc9ba4cad035862a81d30"
a = discrete_log(A, g)
shared_secret = int(power_mod(B, a, p))
print(decrypt_flag(shared_secret, iv, encrypted_flag))



