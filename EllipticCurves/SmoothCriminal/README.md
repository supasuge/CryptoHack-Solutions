# Smooth criminal writeup

This challenge revolves around ECC and the Diffie-Hellman Key Exchange (ECDH) + AES-CBC encryption.

Here's a breakdown of the code:

- An elliptic curve is defined by the equation: $y^{2} = x^{3} + ax + b \mod p$
- Curve parameters:

