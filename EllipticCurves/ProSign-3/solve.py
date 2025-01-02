from pwn import *

import json

import hashlib

from Crypto.Util.number import bytes_to_long, long_to_bytes

from ecdsa.ecdsa import Public_key, Private_key, Signature, generator_192

from random import randrange
#from sage.all import inverse_mod, Matrix

g = generator_192

n = g.order()


class Challenge():

    def __init__(self, s):

        self.before_input = "Welcome to ProSign 3. You can sign_time or verify.\n"

        secret = s

        self.pubkey = Public_key(g, g * secret)

        self.privkey = Private_key(self.pubkey, secret)


    def sha1(self, data):

        sha1_hash = hashlib.sha1()

        sha1_hash.update(data)

        return sha1_hash.digest()


    def sign(self, msg):

        hsh = self.sha1(msg.encode())

        sig = self.privkey.sign(bytes_to_long(hsh), randrange(1, n))

        return {"msg": msg, "r": hex(sig.r), "s": hex(sig.s)}


r = remote("socket.cryptohack.org", 13381)

r.recv()



r.sendline('{"option":"sign_time"}')

first = json.loads(r.recvuntil(b'\n'))

r.sendline('{"option":"sign_time"}')

second = json.loads(r.recvuntil(b'\n'))


print(first)

print(second)

print("run this in sage:")

print("-"*40)

#https://www.reddit.com/r/crypto/comments/h7cr6a/ecdsa_handle_with_care/

#https://blog.trailofbits.com/2020/06/11/ecdsa-handle-with-care/
print(f"""
order = {n} 

r1 = {first['r']}

s1 = {first['s']}

s1_inv = inverse_mod(s1, order)

z1 = {bytes_to_long(hashlib.sha1(first['msg'].encode()).digest())}

r2 = {second['r']}

s2 = {second['s']}

s2_inv = inverse_mod(s2, order)

z2 = {bytes_to_long(hashlib.sha1(second['msg'].encode()).digest())}


matrix = [[order, 0, 0, 0], [0, order, 0, 0],

[r1*s1_inv, r2*s2_inv, (2^96) / order, 0],

[z1*s1_inv, z2*s2_inv, 0, 2^96]]

sol = Matrix(matrix).LLL()

r1_inv = inverse_mod(r1, order)

row = sol[2]

potential_nonce_1 = (row[0])%order

potential_priv_key = (r1_inv * ((potential_nonce_1 * s1) - z1))%order

print("the secret is: ",potential_priv_key)
""")

print("-"*40)

j = Challenge(int(input("Seceret: "))).sign("unlock")

j["option"] = 'verify'

r.sendline(str(j).replace("'",'"'))

r.interactive()
