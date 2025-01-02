#!/usr/bin/python3
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

file = '2048-rsa-example-cert.der'

with open(file, 'rb') as f:
    data = f.read()

cert = x509.load_der_x509_certificate(data, default_backend())

public_key = cert.public_key()

if isinstance(public_key, rsa.RSAPublicKey):
    pub = public_key.public_numbers()
    n = pub.n
    e = pub.e
    print(f"Modulus: {n}")
else:
    print("The public key is not an RSA public key.")
