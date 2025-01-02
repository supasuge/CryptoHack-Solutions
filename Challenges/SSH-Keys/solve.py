import base64
import struct

def read_uint32(data, idx):
    """Read a 4-byte big-endian unsigned integer from data starting at idx."""
    return struct.unpack('>I', data[idx:idx+4])[0], idx+4

def read_bytes(data, idx, length):
    """Read length bytes from data starting at idx."""
    return data[idx:idx+length], idx+length

def read_string(data, idx):
    """Read an SSH string (uint32 length + bytes)."""
    length, idx = read_uint32(data, idx)
    s, idx = read_bytes(data, idx, length)
    return s, idx

def read_mpint(data, idx):
    """Read an mpint (SSH multiple-precision integer)."""
    length, idx = read_uint32(data, idx)
    mpint_bytes, idx = read_bytes(data, idx, length)
    # Convert mpint_bytes to integer
    mpint_int = int.from_bytes(mpint_bytes, 'big', signed=False)
    return mpint_int, idx

def main():
    # Read the SSH public key file
    with open('bruce_rsa.pub', 'r') as f:
        key_line = f.read().strip()

    # Split the key line into parts
    parts = key_line.strip().split()
    if len(parts) < 2:
        print("Invalid SSH public key format.")
        return

    key_type = parts[0]
    key_data_base64 = parts[1]
    comment = ' '.join(parts[2:]) if len(parts) > 2 else ''

    # Decode the base64 key data
    key_data = base64.b64decode(key_data_base64)

    # Parse the key data
    idx = 0

    # Read the key type string
    key_type_string, idx = read_string(key_data, idx)

    # Verify that the key type matches
    if key_type_string != b'ssh-rsa':
        print("Unexpected key type in key data:", key_type_string.decode())
        return

    # Read the exponent e (mpint)
    e, idx = read_mpint(key_data, idx)

    # Read the modulus n (mpint)
    n, idx = read_mpint(key_data, idx)

    # Print the modulus n as a decimal integer
    print(f"Modulus n:\n{n}")

    # Optionally, print the exponent e
    print(f"Exponent e:\n{e}")

if __name__ == '__main__':
    main()
