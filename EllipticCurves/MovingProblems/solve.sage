from sage.all import *
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii

def get_embedding_degree(q, n, max_k):
    for k in range(1, max_k + 1):
        if Integer(q**k - 1) % n == 0:
            return k
    return None

def mov_attack(E, G, P, q, n, max_k=6):
    # Step 2: Find the embedding degree k
    k = get_embedding_degree(q, n, max_k)
    if k is None:
        print("Failed to find a suitable embedding degree.")
        return None

    print(f"Embedding degree k: {k}")

    # Extend the field to GF(q^k)
    Fqk = GF(q**k)
    Ek = E.change_ring(Fqk)
    Gk = Ek(G)
    Pk = Ek(P)

    # Step 3: Find a point Q of order n
    # Since n divides q^k - 1, we can work in the multiplicative group of Fqk
    for _ in range(10):
        # Random point Q in Ek
        Q = Ek.random_point()
        m = Q.order()
        d = gcd(m, n)
        Q = (m // d) * Q
        if Q.order() == n:
            break
    else:
        print("Failed to find a point Q of order n.")
        return None

    # Step 4: Compute the Weil pairing
    alpha = Gk.weil_pairing(Q, n)
    beta = Pk.weil_pairing(Q, n)

    if alpha == 1:
        print("Weil pairing alpha is 1, cannot proceed.")
        return None

    # Step 5: Solve the DLP in Fqk*
    # Compute discrete log of beta to the base alpha
    try:
        n_a = discrete_log(beta, alpha, ord=n)
        return int(n_a)
    except ValueError:
        print("Failed to compute discrete logarithm.")
        return None

def main():
    # Given parameters
    p = 1331169830894825846283645180581
    a = -35
    b = 98

    E = EllipticCurve(GF(p), [a, b])

    # Given points
    G = E(479691812266187139164535778017, 568535594075310466177352868412)
    P1 = E(1110072782478160369250829345256, 800079550745409318906383650948)
    P2 = E(1290982289093010194550717223760, 762857612860564354370535420319)

    # Encrypted data
    iv_hex = 'eac58c26203c04f68d63dc2c58d79aca'
    ciphertext_hex = 'bb9ecbd3662d0671fd222ccb07e27b5500f304e3621a6f8e9c815bc8e4e6ee6ebc718ce9ca115cb4e41acb90dbcabb0d'

    iv = binascii.unhexlify(iv_hex)
    ciphertext = binascii.unhexlify(ciphertext_hex)

    # Step 1: Compute the order of G
    n = G.order()
    print(f"Order of G: {n}")

    # Step 2 to 5: Perform the MOV attack to find n_a
    q = p
    n_a = mov_attack(E, G, P1, q, n, max_k=6)
    if n_a is None:
        print("MOV attack failed.")
        return

    print(f"Computed n_a: {n_a}")

    # Step 6: Compute the shared secret S = n_a * P2
    S = n_a * P2
    shared_secret = int(S.xy()[0])
    print(f"Shared secret: {shared_secret}")

    # Step 7: Derive the AES key
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]

    # Step 8: Decrypt the ciphertext
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), 16)
    print(f"Decrypted flag: {plaintext.decode()}")

if __name__ == '__main__':
    main()
