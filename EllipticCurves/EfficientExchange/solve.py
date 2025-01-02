from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

# Given values
p = 9739
a = 497
b = 1768
x_QA = 4726
nB = 6534

# Calculate y^2 = x^3 + ax + b mod p
y_squared = (x_QA**3 + a * x_QA + b) % p

# Calculate possible y values
def modular_sqrt(a, p):
    return pow(a, (p + 1) // 4, p)

y1 = modular_sqrt(y_squared, p)
y2 = p - y1

# Choose one y value to compute the shared secret
# We can use y1 or y2, here we'll choose y1 arbitrarily
y_QA = y1

# Compute shared secret as nB * (x_QA, y_QA)
# Here we're only interested in the x coordinate of the result
shared_secret = (nB * x_QA) % p

# Decryption details
iv = 'cd9da9f1c60925922377ea952afc212c'
encrypted_flag = 'febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8'

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
        return plaintext

# Decrypt the flag
print(decrypt_flag(shared_secret, iv, encrypted_flag))

