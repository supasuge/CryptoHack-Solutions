#!/usr/bin/python3
from pwn import *
import json

io = remote('socket.cryptohack.org', 13379)
alice_suite = io.recvline().strip().decode().split("e: ")[1]
alice_suite = json.loads(alice_suite)
print(f"Alice suite: {alice_suite}")
alice_suite["supported"] = alice_suite["supported"][-1:]
io.sendline(json.dumps(alice_suite).encode())

bob_suite = io.recvline().strip().decode().split("b: ")[2]
bob_suite = json.loads(bob_suite)
print(bob_suite)
io.sendline(json.dumps(bob_suite).encode())
alice_secret = io.recvline().strip().decode().split("e: ")[2]

alice_secret = json.loads(alice_secret)


bob_secret = io.recvline().strip().decode().split("b: ")[1]

bob_secret = json.loads(bob_secret)


flag = io.recvline().strip().decode().split("e: ")[1]

flag = json.loads(flag)


io.close()


g = int(alice_secret["g"], 16)

p = int(alice_secret["p"], 16)

A = int(alice_secret["A"], 16)

B = int(bob_secret["B"], 16)

iv = flag['iv']

encrypted_flag = flag['encrypted_flag']


print("g =", g)

print("p =", p)

print("A =", A)

print("B =", B)

print("iv =", iv)

print("encrypted_flag =", encrypted_flag)
