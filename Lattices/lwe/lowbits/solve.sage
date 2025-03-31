n = 64
# plaintext modulus
p = 257
# ciphertext modulus
q = 0x10001
# bound for error term
error_bound = int(floor((q/p)/2))
V = VectorSpace(GF(q), n)
# Decryption:
S =  vector(ZZ, [10082, 48747, 17960, 55638, 37012, 51876, 10128, 37750, 7608, 58952, 33296, 25463, 38900, 85, 65248, 42153, 44966, 31594, 40676, 56828, 30325, 38502, 65083, 7497, 2667, 54022, 24029, 32162, 57267, 12253, 6668, 5181, 14906, 51655, 61347, 4722, 22227, 23606, 63183, 52860, 1670, 31085, 42633, 47197, 7255, 16150, 9574, 62956, 26742, 57998, 49467, 31224, 60073, 12730, 41419, 41042, 53032, 16339, 32913, 16351, 34283, 47845, 3617, 35718])

A =  vector(ZZ, [53751, 21252, 55954, 16345, 60990, 2822, 56279, 37048, 36153, 52141, 2121, 56565, 48112, 43755, 12951, 22539, 29478, 28421, 62175, 10265, 36378, 21305, 42402, 26359, 939, 60690, 1161, 65097, 34505, 19777, 29652, 42868, 49148, 38296, 31916, 25606, 18700, 12655, 35631, 64674, 29018, 21021, 14865, 40196, 14036, 40278, 37209, 35585, 34344, 33030, 285, 58536, 56121, 40899, 24262, 62326, 57433, 5765, 24456, 28859, 45170, 14799, 21567, 55484])
b =  11507

"""
1. compute x = (b - A.dot_product(S)) % q
2. interpret x as integer (not mod q), then remove scaling and noise Note: this centered modular reduction must produce a result between (−q/2,q/2](−q/2,q/2] as opposed to usual modular reduction producing a result between [0,q−1][0,q−1]
3. compute m = x mod p
"""
def decrypt(S, ciphertext):
    A, b = ciphertext
    q_half = q // 2
    
    # Step 1: Compute raw difference
    x = (b - A.dot_product(S)) % q
    
    # Step 2: Perform centered modular reduction [-q/2, q/2)
    if x > q_half:
        x = x - q  # bring into the negative range
    
    # Now x \in (-q/2, q/2]

    # Step 3: Recover plaintext m by reducing modulo p
    m_recovered = Integer(x % p)
    
    return m_recovered
ciphertext = (A, b)
m_recovered = decrypt(S, ciphertext)
print("m_recovered:", m_recovered)