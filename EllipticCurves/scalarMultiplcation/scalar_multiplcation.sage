# Define the finite field
p = 9739
F = GF(p)

# Define the elliptic curve
E = EllipticCurve(F, [497, 1768])

# Define the point P
P = E(2339, 2213)

# Implement the Double-and-Add algorithm
def double_and_add(P, n):
    Q = P
    R = E(0)  # Point at infinity (identity element)
    while n > 0:
        if n % 2 == 1:
            R = R + Q
        Q = 2 * Q
        n = n // 2
    return R

# Calculate [7863]P
n = 7863
Q = double_and_add(P, n)

print(f"Q = [7863]P = {Q}")

# Verify that Q is on the curve
assert Q in E, "Q is not on the curve"

# Format the answer
x, y = Q.xy()
answer = f"crypto{{{x}.{y}}}"
print(f"Answer: {answer}")

# Additional verification
X = E(5323, 5438)
assert double_and_add(X, 1337) == E(1089, 6931), "Verification failed"
