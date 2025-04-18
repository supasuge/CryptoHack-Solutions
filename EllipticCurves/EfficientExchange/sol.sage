from sage.all import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

# Define the curve parameters
p = 9739
F = GF(p)
E = EllipticCurve(F, [497, 1768])
G = E(1804, 5368)

# Alice's public key x-coordinate and Bob's secret
x_QA = 4726
nB = 6534

# Function to find y given x on the curve
def find_y(x):
    y_squared = (x^3 + 497*x + 1768) % p
    # Since p ≡ 3 (mod 4), we can use the formula y = ±y_squared^((p+1)/4) mod p
    y = pow(y_squared, (p+1)//4, p)
    return y

# Find y coordinate of QA
y_QA = find_y(x_QA)

# Create the point QA
QA = E(x_QA, y_QA)

# Calculate the shared secret
S = nB * QA
shared_secret = S[0]  # We only need the x-coordinate

print(f"Shared secret: {shared_secret}")

# Decryption function (as provided)
def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')

# Decrypt the flag
iv = 'cd9da9f1c60925922377ea952afc212c'
ciphertext = 'febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8'

flag = decrypt_flag(shared_secret, iv, ciphertext)
print(f"Flag: {flag}")
