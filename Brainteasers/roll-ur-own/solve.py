#!/usr/bin/env python3
"""
solve_remote.py

Connect to the Cryptohack “get_bit” oracle, recover each of the 256 bits
of the 32‑byte flag by subgroup‑membership testing, and reassemble/print it.
"""

import socket
import json
import argparse

# ─── PARAMETERS ───────────────────────────────────────────────────────────────

HOST = "socket.cryptohack.org"
PORT = 13398

# From the challenge source:
N = 561358413744886843732586944232928827094785116282248238064188105967202946842534189427044181790919978255516478660622865024411901150277082224606620707791759947017884280039090103820456132072845327917418736737030666331194466104006934585291004296083372192319606579530917382712591915541173133966427632108600606391410738465748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540
phi = 561358413744886843732586944232928827094785116282248238064188105967202946842534189427044181790919978255516478660622865024411901150277082224606620707791759947017884280039090103820456132072845327917418736737030666331194466104006934585291004296083372192319606579530917382712591915541173133966427632108600606391410738465748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540636395665748540
FLAG_BYTE_LEN = 32  # the challenge comment says “Flag is 32 bytes long”

# ─── HELPERS ─────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description="Recover flag via the get_bit oracle")
    p.add_argument("--host",  default=HOST, help="Oracle host")
    p.add_argument("--port",  default=PORT, type=int, help="Oracle port")
    p.add_argument("--bytes", "-n", default=FLAG_BYTE_LEN, type=int,
                   help="Length of the flag in bytes")
    return p.parse_args()

def recv_line(f):
    """Read one line (terminated by '\\n') from socket‑file f."""
    line = f.readline()
    if not line:
        raise EOFError("Connection closed unexpectedly")
    return line.strip()

def get_oracle_bit(f, idx):
    """
    Ask the oracle for bit index idx; return the raw integer x.

    The server expects:
        {"option":"get_bit","i":"<idx>"}
    and replies
        {"bit":"0x..."}
    """
    req = {"option": "get_bit", "i": str(idx)}
    f.write(json.dumps(req) + "\n")  # send and flush
    f.flush()
    resp = json.loads(recv_line(f))
    if "bit" not in resp:
        raise ValueError(f"Unexpected oracle response: {resp}")
    return int(resp["bit"], 16)

def is_in_subgroup(x):
    """
    Recover the hidden bit by subgroup‑membership:
      g has order φ(N)/2 mod N, so
          x^(φ(N)/2) ≡ 1      ⇒ bit=1
          x^(φ(N)/2) ≡ N-1    ⇒ bit=0  (with overwhelming probability)
    """
    return pow(x, phi // 2, N) == 1

# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    args = parse_args()

    # 1) Connect and wrap in a file-like interface
    sock = socket.create_connection((args.host, args.port))
    f = sock.makefile("rw", buffering=1, encoding="utf-8")

    # 2) Read welcome banner
    banner = recv_line(f)
    print(banner)

    total_bits = args.bytes * 8
    bits = [0] * total_bits

    # 3) Query every bit
    for i in range(total_bits):
        x = get_oracle_bit(f, i)     # raw oracle output
        bits[i] = 1 if is_in_subgroup(x) else 0

        # progress
        byte_i, bit_i = divmod(i, 8)
        print(f"\rRecovered bit {i:3d} (byte {byte_i}, bit {bit_i}): {bits[i]}", end="")

    print("\nAll bits recovered; assembling flag…")

    # 4) Pack bits (little-endian within each byte) → bytes → ASCII
    flag_bytes = bytearray(args.bytes)
    for i, b in enumerate(bits):
        flag_bytes[i // 8] |= b << (i % 8)

    flag = flag_bytes.decode("utf-8", errors="replace")
    print("FLAG:", flag)

if __name__ == "__main__":
    main()
