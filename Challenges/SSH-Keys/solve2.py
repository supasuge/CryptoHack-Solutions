from cryptography.hazmat.primitives import serialization
import os

def convert_to_pem():
    os.system(f"ssh-keygen -f bruce_rsa.pub -e -m PEM > bruce_rsa.pem")



def main():
    convert_to_pem()
    # Read the PEM file
    with open('bruce_rsa.pem', 'rb') as f:
        pem_data = f.read()
    
    # Load the public key
    public_key = serialization.load_pem_public_key(pem_data)
    
    # Ensure it's an RSA key
    if not hasattr(public_key, 'public_numbers'):
        print("The key is not an RSA public key.")
        return
    
    numbers = public_key.public_numbers()
    n = numbers.n
    e = numbers.e
    
    # Print the modulus and exponent
    print(f"Modulus n:\n{n}")
    print(f"Exponent e:\n{e}")

if __name__ == '__main__':
    main()

