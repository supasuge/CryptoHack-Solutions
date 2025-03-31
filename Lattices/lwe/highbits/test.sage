#!/usr/local/bin/sage
# -*- coding: utf-8 -*-

# parameters
# n = vector space
# q = ciphertext modulus
# p = plaintext modulus (can only encrypt m < p)
# scaling factor Delta = round(q/p)


# key-gen
# S = random element of the vector space ZZ^n_q
# S = secret key

# Ciphertext formula
# A, b where A is an element of the vector space ZZ^n_q, and b is an element of ZZ_q

# encryption
# Sample A, a random element of the vector space ZZ^n_q
# sample the error-term e, an integer in the range [-Delta/2, Delta/2] Note: often the error is sample from a discrete gaussian distribution, but uniform sampling is also possible
# compute b = <A, S> + Delta * m + e
# return the pair (A, b) as the ciphertext

n = 10
q = 3329
p = 17
Delta = round(q/p)
Zq = IntegerModRing(q)
V = VectorSpace(Zq, n)

def key_gen():
    S = V.random_element()
    return S

def encrypt(S, m):
    A = V.random_element()
    e = randint(-Delta//2, Delta//2)
    b = (A.dot_product(S) + Delta * m + e) % q
    return (A, b)

def decrypt(S, ciphertext):
    A, b = ciphertext
    x = (b - A.dot_product(S)) % q

    # Interpret x as integer (not mod q), then remove scaling and noise
    # Round to nearest integer to remove error e
    m_recovered = round(Integer(x) / Delta)

    return m_recovered

S = key_gen()
print("S:", S)
m = 5
print("m:", m)
ciphertext = encrypt(S, m)
print("Ciphertext:", ciphertext)
m_recovered = decrypt(S, ciphertext)
print("m_recovered:", m_recovered)
assert m == m_recovered, "Decryption failed!"
print("Decryption successful!")
