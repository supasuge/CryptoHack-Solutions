#!/usr/bin/env python3

from pwn import *
import re
from fastecdsa.curve import P256
from fastecdsa.point import Point

from util import mod_inv, p256_mod_sqrt

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from tqdm import tqdm

def find_point_on_curve(x_candidate):
    p = P256.p
    a = P256.a
    b = P256.b
    y_squared = (pow(x_candidate, 3, p) + a * x_candidate + b) % p
    try:
        y = pow(y_squared, (p + 1) // 4, p)
        if pow(y, 2, p) == y_squared:
            return True, y
    except ValueError:
        pass
    return False, None

def gen_prediction(observed, Qx, Qy, d):
    Q = Point(Qx, Qy, curve=P256)
    P = P256.G
    e = mod_inv(d, P256.q)
    checkbits = observed & 0xffff

    for high_bits in tqdm(range(2**16)):
        guess = (high_bits << (8 * 30)) | (observed >> (8 * 2))
        on_curve, y = find_point_on_curve(guess)

        if on_curve:
            point = Point(guess, y, curve=P256)
            t_candidate = (e * point).x % P256.p
            s_point = t_candidate * P
            s = s_point.x % P256.p
            r_point = s * Q
            r = r_point.x % P256.p
            r_bits = r & (2**(8 * 30) - 1)

            if (r >> (8 * 28)) == checkbits:
                return r_bits
    return None

def main():
    # Connect to the challenge server using pwntools
    HOST = 'localhost'
    PORT = 1337

    # Use pwntools remote connection
    io = remote(HOST, PORT)

    # Receive all data until EOF
    data = io.recvall().decode()
    print(f"Data received:{data}")
    io.close()

    # Extract data using regex
    observed_hex = re.search(r'Observed 32 bytes \(hex\):\n([0-9a-fA-F]{64})', data).group(1)
    if not observed_hex:
        print("Failed to extract observed data.")
        sys.exit(1)
    else:
        print(f"Observed hex: {observed_hex}")
    Qx_hex = re.search(r'Q\.x = ([0-9a-fA-F]{64})', data).group(1)
    if not Qx_hex:
        print("Failed to extract Qx.")
        sys.exit(1)
    else:
        print(f"Qx hex: {Qx_hex}")
    
    Qy_hex = re.search(r'Q\.y = ([0-9a-fA-F]{64})', data).group(1)
    if not Qy_hex:
        print("Failed to extract Qy.")
        sys.exit(1)
    else:
        print(f"Qy hex: {Qy_hex}")
    
    encrypted_flag_hex = re.search(r'Encrypted flag \(hex\):\n([0-9a-fA-F]+)', data).group(1)
    if not encrypted_flag_hex:
        print("Failed to extract encrypted flag.")
        sys.exit(1)
    else:
        print(f"Encrypted flag hex: {encrypted_flag_hex}")
    observed = int(observed_hex, 16)
    if not observed:
        print("Failed to convert observed data to integer.")
        sys.exit(1)
    else:
        print(f"Observed: {observed}")
    Qx = int(Qx_hex, 16)
    Qy = int(Qy_hex, 16)
    Q = Point(Qx, Qy, curve=P256)
    encrypted_flag = bytes.fromhex(encrypted_flag_hex)
    if not encrypted_flag:
        print("Failed to convert encrypted flag to bytes.")
        sys.exit(1)
    else:
        print(f"Encrypted flag: {encrypted_flag_hex}")

    P = P256.G

    # Compute d = discrete_log(P, Q) for small d
    max_d = 2**16
    d = None
    print("Computing discrete logarithm...")
    for i in tqdm(range(2, max_d)):
        if i * P == Q:
            d = i
            print(f"Found d: {d}")
            break
    if d is None:
        print("Failed to compute d.")
        sys.exit(1)

    # Predict the next output
    predicted_bits = gen_prediction(observed, Qx, Qy, d)
    if predicted_bits is None:
        print("Failed to predict the next output.")
        sys.exit(1)

    # Derive AES key
    key_material = predicted_bits & (2**(8 * 16) -1)  # Use lower 16 bytes as AES key
    key = key_material.to_bytes(16, 'big')

    # Decrypt the flag
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = unpad(cipher.decrypt(encrypted_flag), 16)
    print("Decrypted Flag:")
    print(decrypted.decode())

if __name__ == '__main__':
    main()
