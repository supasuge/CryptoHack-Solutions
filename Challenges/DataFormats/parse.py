from Crypto.PublicKey import RSA

# Replace 'privacy_enhanced_mail.pem' with the path to your PEM file
pem_file = 'privenhancedmail.pem'

# Read the PEM file
with open(pem_file, 'r') as f:
    pem_data = f.read()

# Import the RSA key
key = RSA.import_key(pem_data)

# Check if the key is a private key
if not key.has_private():
    print("The provided key is not a private key.")
    exit(1)

# Extract RSA key components
n = key.n  # Modulus
e = key.e  # Public exponent
d = key.d  # Private exponent
p = key.p  # First prime factor
q = key.q  # Second prime factor

# Print the private exponent 'd' as a decimal integer

print(f"Private exponent d: {d}")

