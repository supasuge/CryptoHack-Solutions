#!/usr/bin/env python3

import os
import sys
from random import randint

from fastecdsa.curve import P256
from fastecdsa.point import Point

from util import p256_mod_sqrt, mod_inv

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

FLAG = open('flag.txt', 'r').read().strip()

def gen_backdoor():
    P = P256.G  # Base point
    d = randint(2, 2**16)  # Small secret scalar for the backdoor
    e = mod_inv(d, P256.q)
    Q = e * P  # Public point Q

    return P, Q, d

class DualEC():
    def __init__(self, seed, P, Q):
        self.seed = seed
        self.P = P
        self.Q = Q

    def genbits(self):
        t = self.seed
        s_point = t * self.P
        s = s_point.x % P256.p
        self.seed = s
        r_point = s * self.Q
        r = r_point.x % P256.p
        return r & (2**(8 * 30) - 1)  # Return 30 bytes

def main():
    P, Q, d = gen_backdoor()
    # Random seed
    seed = int.from_bytes(os.urandom(32), 'big') % P256.q
    dualec = DualEC(seed, P, Q)
    bits1 = dualec.genbits()  # First output
    bits2 = dualec.genbits()  # Second output

    observed = (bits1 << (2 * 8)) | (bits2 >> (28 * 8))  # Observed 32 bytes

    # Output observed data
    print('Observed 32 bytes (hex):')
    print('{:064x}'.format(observed))

    # Output Q
    print('Q point coordinates:')
    print('Q.x = {:064x}'.format(Q.x))
    print('Q.y = {:064x}'.format(Q.y))

    # Encrypt the flag
    key_material = bits2 & (2**(8 * 16) -1)  # Use lower 16 bytes as AES key
    key = key_material.to_bytes(16, 'big')
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(FLAG.encode(), 16))
    print('Encrypted flag (hex):')
    print(ciphertext.hex())

if __name__ == '__main__':
    try:
        main()
    except BrokenPipeError:
        sys.exit(0)
