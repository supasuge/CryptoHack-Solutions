import requests

BASE_URL = 'https://aes.cryptohack.org'

def encrypt(key, plaintext):
    url = f'{BASE_URL}/triple_des/encrypt/{key}/{plaintext}/'
    response = requests.get(url)
    return response.json()

def encrypt_flag(key):
    url = f'{BASE_URL}/triple_des/encrypt_flag/{key}/'
    response = requests.get(url)
    return response.json()

def main():
    # Known plaintext: 'crypto{' in hex
    known_plaintext_hex = '63727970746f7b'

    # Try encrypting known plaintext with different keys
    # (You'll need to brute force or attempt guesses here)
    for key_guess in range(0, 0xFFFFFFFF):  # Example: trying all possible keys (adjust as necessary)
        key_hex = f'{key_guess:016x}'  # Ensure key is 16 hex characters
        encrypted_data = encrypt(key_hex, known_plaintext_hex)
        if 'ciphertext' in encrypted_data:
            ciphertext = encrypted_data['ciphertext']
            print(f'Key: {key_hex}, Ciphertext: {ciphertext}')

        # If ciphertext matches a target value or you can deduce something, proceed

    # Eventually, when you find the right key:
    flag_encrypted = encrypt_flag(key_hex)
    print(f'Flag: {flag_encrypted}')

if __name__ == '__main__':
    main()
