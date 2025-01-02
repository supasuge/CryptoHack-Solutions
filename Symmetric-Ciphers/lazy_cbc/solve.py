import requests

BASE_URL = 'https://aes.cryptohack.org'  # Replace with the actual base URL

def encrypt(plaintext_hex):
    url = f'{BASE_URL}/lazy_cbc/encrypt/{plaintext_hex}/'
    response = requests.get(url)
    data = response.json()
    return data

def receive(ciphertext_hex):
    url = f'{BASE_URL}/lazy_cbc/receive/{ciphertext_hex}/'
    response = requests.get(url)
    data = response.json()
    return data

def get_flag(key_hex):
    url = f'{BASE_URL}/lazy_cbc/get_flag/{key_hex}/'
    response = requests.get(url)
    data = response.json()
    return data

def main():
    # Step 1: Encrypt two blocks of zeros
    plaintext_hex = '00' * 32  # 32 bytes of zeros
    encrypt_response = encrypt(plaintext_hex)
    if 'ciphertext' not in encrypt_response:
        print('Encryption error:', encrypt_response)
        return
    ciphertext_hex = encrypt_response['ciphertext']
    # Step 2: Prepare modified ciphertext
    c0 = ciphertext_hex[:32]  # First block (16 bytes)
    c0_prime = '00' * 16  # 16 bytes of zeros
    modified_ciphertext_hex = c0_prime + c0
    # Step 3: Submit modified ciphertext
    receive_response = receive(modified_ciphertext_hex)
    if 'error' not in receive_response:
        print('Receive error:', receive_response)
        return
    error_message = receive_response['error']
    # Step 4: Extract the KEY
    prefix = 'Invalid plaintext: '
    if not error_message.startswith(prefix):
        print('Unexpected error message:', error_message)
        return
    decrypted_hex = error_message[len(prefix):]
    if len(decrypted_hex) < 64:
        print('Decrypted plaintext too short')
        return
    p1_prime_hex = decrypted_hex[32:64]  # Second block
    key_hex = p1_prime_hex
    print(f"Recovered KEY (hex): {key_hex}")
    # Step 5: Get the flag
    get_flag_response = get_flag(key_hex)
    if 'plaintext' in get_flag_response:
        flag_hex = get_flag_response['plaintext']
        flag_bytes = bytes.fromhex(flag_hex)
        flag = flag_bytes.decode('utf-8')
        print('FLAG:', flag)
    else:
        print('Failed to get flag:', get_flag_response)

if __name__ == '__main__':
    main()

