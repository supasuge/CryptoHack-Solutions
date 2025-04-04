from pwn import *
import json

host = "socket.cryptohack.org"
port = 13403


def main():
    s = remote(host, port)

    
    s.recvuntil(b'Prime generated: ')
    q_hex = s.recvline().decode().strip().replace('"', '')
    q = int(q_hex, 16)
    print(f"[+] Received q: {q}")

    
    g, n = q + 1, q * q
    assert pow(g, q, n) == 1, "Invalid parameters"

    params = json.dumps({"g": hex(g), "n": hex(n)}).encode()
    s.sendline(params)
    print(f"[+] Sent params: {params}")

    # Receive public key
    s.recvuntil(b'Generated my public key: ')
    h_hex = s.recvline().decode().strip().replace('"', '')
    h = int(h_hex, 16)
    print(f"[+] Received h: {h}")

    # solve for x
    x = (h - 1) // q
    assert pow(g, x, n) == h, "Verification failed"

    answer = json.dumps({"x": hex(x)}).encode()
    s.sendline(answer)
    print(f"[+] Sent solution: {answer}")

    #get flag
    response = s.recvline().decode()
    try:
        flag = json.loads(response)['flag']
        print(f"[+] Flag: {flag}")
    except (json.JSONDecodeError, KeyError):
        print(f"[-] Unexpected response: {response}")

    s.close()


if __name__ == '__main__':
    main()
