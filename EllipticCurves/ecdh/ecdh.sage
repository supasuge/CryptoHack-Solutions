# ECDLP is the problem of finding an integer $n$ such that $Q = [n]P$.



# Like encountered with the discrete logarithm problem, scalar multiplcationof a point in $E(f_p$ seems to be a hard problem to undo with the most efficient algorithm running $q^{1/2}$ time when $P$ generates a subgroup of size $q$


# This makes it a great candidate for a trapdoor function.




# Define the finite field
p = 9739
F = GF(p)

# Define the elliptic curve
E = EllipticCurve(F, [497, 1768])

# Define the generator point G
G = E(1804, 5368)

# Define Alice's public key QA
QA = E(815, 3190)

# Define Bob's secret key nB
nB = 1829

# Calculate the shared secret S = [nB]QA
S = nB * QA

print(f"Shared secret S: {S}")

# Extract the x-coordinate of S
x_coord = S[0]

# Convert the x-coordinate to a string
x_coord_str = str(x_coord)

# Calculate the SHA1 hash of the x-coordinate
import hashlib
hash_object = hashlib.sha1(x_coord_str.encode())
hex_dig = hash_object.hexdigest()

# Format the answer
answer = f"crypto{{{hex_dig}}}"
print(f"Answer: {answer}")
