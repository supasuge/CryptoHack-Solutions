import requests
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

BASE_URL = 'https://aes.cryptohack.org'

def get_ciphertext(key_hex):
    response = requests.get(f'{BASE_URL}/triple_des/encrypt_flag/{key_hex}/')
    json_response = response.json()
    if 'ciphertext' in json_response:
        return bytes.fromhex(json_response['ciphertext'])
    else:
        # Print the error message from the server
        print("Error:", json_response['error'])
        raise Exception("Failed to get ciphertext")

def des3_encrypt(key, plaintext):
    cipher = DES3.new(key, DES3.MODE_ECB)
    return cipher.encrypt(plaintext)

def recover_iv(ciphertext, known_plaintext, key):
    iv_candidates = []

    def recurse(iv_prefix, depth):
        if depth == 8:
            iv = bytes(iv_prefix)
            P_input = bytes([kp ^ ivb for kp, ivb in zip(known_plaintext, iv)])
            E_output = des3_encrypt(key, P_input)
            C_check = bytes([e ^ ivb for e, ivb in zip(E_output, iv)])
            if C_check == ciphertext:
                iv_candidates.append(iv)
            return

        for iv_byte in range(256):
            iv_candidate = iv_prefix + [iv_byte]
            iv = bytes(iv_candidate + [0]*(7 - depth))
            P_input = bytes([kp ^ ivb for kp, ivb in zip(known_plaintext[:depth+1], iv[:depth+1])]) + b'\x00'*(7 - depth)
            E_output = des3_encrypt(key, P_input)
            C_partial = bytes([e ^ ivb for e, ivb in zip(E_output[:depth+1], iv[:depth+1])])
            if C_partial == ciphertext[:depth+1]:
                recurse(iv_candidate, depth + 1)

    recurse([], 0)
    return iv_candidates[0] if iv_candidates else None

def main():
    # Generate a valid 16-byte key and adjust parity bits
    while True:
        key = get_random_bytes(16)
        try:
            DES3.new(key, DES3.MODE_ECB)
            break  # Valid key found
        except ValueError:
            continue  # Invalid key, try again

    key_hex = key.hex()
    try:
        ciphertext = get_ciphertext(key_hex)
    except Exception as e:
        print("Could not retrieve ciphertext:", e)
        return

    known_plaintext = b'crypto{\x01'  # Assuming PKCS#7 padding with \x01
    iv = recover_iv(ciphertext, known_plaintext, key)
    if iv:
        # Decrypt the ciphertext to get the flag
        P_input = bytes([c ^ ivb for c, ivb in zip(ciphertext, iv)])
        cipher = DES3.new(key, DES3.MODE_ECB)
        plaintext_xor_iv = cipher.decrypt(P_input)
        flag = bytes([p ^ ivb for p, ivb in zip(plaintext_xor_iv, iv)])
        print("Recovered FLAG:", flag.decode())
    else:
        print("IV not found")

if __name__ == '__main__':
    main()

