from cryptography.hazmat.primitives import serialization

def extract_rsa_parameters(pem_file):
    # Read the PEM file
    with open(pem_file, 'rb') as f:
        pem_data = f.read()
    
    # Load the public key
    public_key = serialization.load_pem_public_key(pem_data)
    
    # Ensure it's an RSA key
    if not hasattr(public_key, 'public_numbers'):
        print("The key is not an RSA public key.")
        return None, None
    
    numbers = public_key.public_numbers()
    n = numbers.n
    e = numbers.e
    
    return n, e

if __name__ == '__main__':
    pem_file = 'transparency.pem'
    n, e = extract_rsa_parameters(pem_file)
    if n and e:
        print(f"Modulus n:\n{n}")
        print(f"Exponent e:\n{e}")

