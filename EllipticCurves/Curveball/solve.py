from pwn import remote, log
import json
from fastecdsa.point import Point
from fastecdsa.curve import P256
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def cprint(message, color=Fore.WHITE, style=Style.NORMAL):
    """
    Helper function to print colored messages.
    
    Args:
        message (str): The message to print.
        color (str): The color of the text.
        style (str): The style of the text.
    """
    print(f"{color}{style}{message}{Style.RESET_ALL}")

def mod_inv(a, m):
    """
    Computes the modular inverse of a modulo m.
    Only works if m is prime (Euler's Theorem).
    
    Args:
        a (int): The number to invert.
        m (int): The modulus.
    
    Returns:
        int: The modular inverse of a modulo m.
    """
    return pow(a, m-2, m)

# Remote connection details
HOST = 'socket.cryptohack.org'
PORT = 13382

def connect_to_service():
    """Establishes a connection to the remote service."""
    try:
        cprint(f"[+] Connecting to {HOST}:{PORT}... [+]\r\n", Fore.CYAN, Style.BRIGHT)
        r = remote(HOST, PORT)
        cprint("[+] Connection established. [+]\r\n", Fore.GREEN)
        return r
    except Exception as e:
        cprint(f"[-] Failed to connect to {HOST}:{PORT} - {e} [-]\r\n", Fore.RED)
        exit(1)

def compute_generator(Q_target, d_prime, curve=P256):
    """
    Computes the generator point 'g' such that g * d_prime = Q_target.
    
    Args:
        Q_target (Point): The target public key to match (Q_bing.com).
        d_prime (int): The chosen small private key.
        curve (Curve): The elliptic curve being used.
    
    Returns:
        Point: The computed generator point 'g'.
    """
    n = curve.q  # Order of the curve
    try:
        inv_d = mod_inv(d_prime, n)
        cprint(f"[+] Computed inverse of d' ({d_prime}) modulo n. [+]", Fore.GREEN)
        cprint(f"[+] Inverse of d' ({d_prime}) modulo n: {inv_d} [+]\r\n", Fore.YELLOW)
    except ValueError:
        cprint("[-] Failed to compute modular inverse. Choose a different d'. [-]\r", Fore.RED)
        exit(1)
    
    # Compute g = Q_target * inv_d
    g = Q_target * inv_d
    cprint(f"[+] Computed generator point 'g' such that g * d' = Q_target. [+]\r\n", Fore.GREEN)
    return g

def craft_packet(host, private_key, generator, curve="secp256r1"):
    """
    Crafts the JSON packet to send to the server.
    
    Args:
        host (str): The hostname to add or query.
        private_key (int): The private key corresponding to the public key.
        generator (Point): The generator point [G.x, G.y].
        curve (str): The curve used.
    
    Returns:
        str: JSON-encoded string.
    """
    packet = {
        "host": host,
        "private_key": private_key,
        "curve": curve,
        "generator": [generator.x, generator.y]
    }
    cprint(f"[+] Crafted JSON packet for host '{host}'. [+]\r\n", Fore.CYAN)
    return json.dumps(packet) + "\n"  # Assuming the server expects newline-delimited JSON

def main():
    # Define Q_bing.com from the server's trusted_certs
    Q_bing_com = Point(
        0x3B827FF5E8EA151E6E51F8D0ABF08D90F571914A595891F9998A5BD49DFA3531,
        0xAB61705C502CA0F7AA127DEC096B2BBDC9BD3B4281808B3740C320810888592A,
        curve=P256
    )
    cprint("[+] Defined target public key Q_bing.com. [+]", Fore.CYAN)
    
    # Choose a small private key d'
    d_prime = 2  # Must be != 1 and != -1
    cprint(f"[+] Selected small private key d' = {d_prime}. [+]\r\n", Fore.CYAN)
    
    # Compute the generator 'g' such that g * d_prime = Q_bing.com
    g = compute_generator(Q_bing_com, d_prime, curve=P256)
    cprint(f"[+] Generator 'g' computed: ({g.x}, {g.y}\n) [+]\r\n", Fore.YELLOW)
    
    # Craft the packet
    # You can choose any host; it doesn't matter as long as Q matches Q_bing.com
    target_host = "attacker.com"
    packet = craft_packet(target_host, d_prime, g, curve="secp256r1")
    
    # Display the crafted packet
    cprint(f"[>] Packet to send:\n{packet}\r[<]\n", Fore.MAGENTA)
    
    # Connect to the remote service
    r = connect_to_service()
    
    # Receive initial welcome message (if any)
    try:
        welcome = r.recvuntil(b'\n').decode().strip()
        cprint(f"[+] Received Welcome Message: {welcome} [+]\r\n", Fore.GREEN)
    except Exception as e:
        cprint(f"[-] Failed to receive welcome message: {e} [-]", Fore.RED)
    
    # Send the crafted packet
    cprint("[>] Sending crafted packet to the server [<]\r\n", Fore.CYAN)
    try:
        r.send(packet.encode())
        cprint("[+] Packet sent successfully. [+]\r\n", Fore.GREEN)
    except Exception as e:
        cprint(f"[-] Failed to send packet: {e} [-]\r\n", Fore.RED)
        r.close()
        exit(1)
    
    # Receive the server's response
    try:
        response = r.recvline().decode().strip()
        cprint(f"[+] Received Response: {response} [+]\r\n", Fore.GREEN)
    except Exception as e:
        cprint(f"[-] Failed to receive response: {e} [-]\r\n", Fore.RED)
        r.close()
        exit(1)
    
    # Check if the response contains the flag
    if "crypto{" in response:
        flag = response.split("crypto{")[1].split("}")[0]
        cprint(f"[+] Flag Retrieved: crypto{{{flag}}} [+]\r\n", Fore.GREEN, Style.BRIGHT)
    else:
        cprint("[!] Flag not found in the response. [!]", Fore.YELLOW)
    
    # Close the connection
    cprint("[*] Closing connection. [*]", Fore.CYAN)
    r.close()
    cprint("[+] Connection closed. [+]", Fore.GREEN)

if __name__ == "__main__":
    main()
