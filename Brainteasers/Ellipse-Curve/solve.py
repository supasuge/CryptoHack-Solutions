#!/usr/bin/env python3
"""
real_flag_exploit.py

Exploit script to recover the actual flag using the provided challenge data.
"""
# try all methods in parallel for effectiveness
import hashlib
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from math import isqrt
from sympy import discrete_log, factorint
from cypari2 import Pari
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# ——— Challenge Parameters ———
p = 173754216895752892448109692432341061254596347285717132408796456167143559
D = 529  # = 23²
G = (
    29394812077144852405795385333766317269085018265469771684226884125940148,
    94108086667844986046802106544375316173742538919949485639896613738390948
)

# ——— Actual Challenge Data ———
alice_public = (155781055760279718382374741001148850818103179141959728567110540865590463, 
                73794785561346677848810778233901832813072697504335306937799336126503714)

bob_public = (171226959585314864221294077932510094779925634276949970785138593200069419,
              54353971839516652938533335476115503436865545966356461292708042305317630)

encrypted_data = {
    'iv': '64bc75c8b38017e1397c46f85d4e332b',
    'encrypted_flag': '13e4d200708b786d8f7c3bd2dc5de0201f0d7879192e6603d7c5d6b963e1df2943e3ff75f7fda9c30a92171bbbc5acbf'
}

# Pre-compute constants for optimization
pari = Pari()
sqrt_D = isqrt(D)  # 23
p_minus_1 = p - 1

class RealFlagExploit:
    """Exploit to recover the actual flag from the challenge."""
    
    def __init__(self, p, D, G):
        self.p = p
        self.D = D
        self.G = G
        self.sqrt_D = sqrt_D  # Use pre-computed value
        self.results = {}  # Store results from parallel execution
        self.generator_fp = None  # Cache generator mapping
        self.alice_fp = None  # Cache Alice's mapping
        self.bob_fp = None  # Cache Bob's mapping
        print(f"🎯 Exploiting Pell conic x² - {D}y² = 1")
        print(f"📊 D = {D} = {self.sqrt_D}² (perfect square - CRITICAL FLAW!)")
        
        # Pre-compute mappings for efficiency
        self._precompute_mappings()
    
    def _precompute_mappings(self):
        """Pre-compute all 𝔽ₚ* mappings to avoid redundant calculations."""
        print("⚡ Pre-computing 𝔽ₚ* mappings...")
        self.generator_fp = self.conic_to_fp_star(self.G)
        self.alice_fp = self.conic_to_fp_star(alice_public)
        self.bob_fp = self.conic_to_fp_star(bob_public)
        print(f"Generator in 𝔽ₚ*: {self.generator_fp}")
        print(f"Alice in 𝔽ₚ*: {self.alice_fp}")
        print(f"Bob in 𝔽ₚ*: {self.bob_fp}")
    
    def point_add(self, P1, P2):
        """Add two points on the Pell conic."""
        x1, y1 = P1
        x2, y2 = P2
        x3 = (x1 * x2 + self.D * y1 * y2) % self.p
        y3 = (x1 * y2 + y1 * x2) % self.p
        return (x3, y3)
    
    def point_scalar_mult(self, k, P):
        """Scalar multiplication using double-and-add."""
        if k == 0:
            return (1, 0)
        
        result = (1, 0)
        addend = P
        k = int(k)  # Ensure k is a Python int
        
        while k:
            if k & 1:
                result = self.point_add(result, addend)
            addend = self.point_add(addend, addend)
            k >>= 1
        
        return result
    
    def conic_to_fp_star(self, point):
        """Map Pell conic point to 𝔽ₚ* element: (x,y) → x + 23y."""
        x, y = point
        return (x + self.sqrt_D * y) % self.p
    
    def recover_private_key_method_1(self, target_public_key, method_name="Baby-step giant-step"):
        """Method 1: Optimized baby-step giant-step in 𝔽ₚ*."""
        print(f"\n🚀 {method_name}: Baby-step giant-step in 𝔽ₚ*")
        
        # Use pre-computed mappings
        if target_public_key == alice_public:
            target_fp = self.alice_fp
        elif target_public_key == bob_public:
            target_fp = self.bob_fp
        else:
            target_fp = self.conic_to_fp_star(target_public_key)
        
        print(f"[{method_name}] Target in 𝔽ₚ*: {target_fp}")
        
        # Optimized limits based on problem size
        limits = [10000, 100000, 1000000]  # Reduced limits for faster execution
        
        for limit in limits:
            print(f"[{method_name}] 🔍 Trying baby-step giant-step with limit {limit}")
            private_key = self.baby_step_giant_step_optimized(self.generator_fp, target_fp, limit)
            
            if private_key is not None:
                print(f"[{method_name}] ✅ Found private key: {private_key}")
                
                # Quick verification
                if self.quick_verify(private_key, target_public_key):
                    print(f"[{method_name}] ✅ Verification successful!")
                    return private_key
                else:
                    print(f"[{method_name}] ❌ Verification failed, continuing search...")
        
        return None
    
    def recover_private_key_method_2(self, target_public_key, method_name="Pollard's rho"):
        """Method 2: Optimized Pollard's rho in 𝔽ₚ*."""
        print(f"\n🚀 {method_name}: Pollard's rho in 𝔽ₚ*")
        
        # Use pre-computed mappings
        if target_public_key == alice_public:
            target_fp = self.alice_fp
        elif target_public_key == bob_public:
            target_fp = self.bob_fp
        else:
            target_fp = self.conic_to_fp_star(target_public_key)
        
        private_key = self.pollard_rho_optimized(self.generator_fp, target_fp, method_name)
        
        if private_key is not None:
            print(f"[{method_name}] ✅ Found private key: {private_key}")
            
            # Quick verification
            if self.quick_verify(private_key, target_public_key):
                print(f"[{method_name}] ✅ Verification successful!")
                return private_key
        
        return None
    
    def recover_private_key_method_3(self, target_public_key, method_name="SymPy"):
        """Method 3: Optimized SymPy discrete_log."""
        print(f"\n🚀 {method_name}: SymPy discrete_log")
        
        # Use pre-computed mappings
        if target_public_key == alice_public:
            target_fp = self.alice_fp
        elif target_public_key == bob_public:
            target_fp = self.bob_fp
        else:
            target_fp = self.conic_to_fp_star(target_public_key)
        
        try:
            private_key = discrete_log(self.p, target_fp, self.generator_fp)
            print(f"[{method_name}] ✅ Found private key: {private_key}")
            
            # Quick verification
            if self.quick_verify(private_key, target_public_key):
                print(f"[{method_name}] ✅ Verification successful!")
                return int(private_key)
        except Exception as e:
            print(f"[{method_name}] ❌ SymPy failed: {e}")
        
        return None
    
    def recover_private_key_method_4(self, target_public_key, method_name="PARI/GP"):
        """Method 4: Optimized PARI/GP discrete log."""
        print(f"\n🚀 {method_name}: PARI/GP discrete log")
        
        # Use pre-computed mappings
        if target_public_key == alice_public:
            target_fp = self.alice_fp
        elif target_public_key == bob_public:
            target_fp = self.bob_fp
        else:
            target_fp = self.conic_to_fp_star(target_public_key)
        
        try:
            pari_p = pari(self.p)
            pari_g = pari(self.generator_fp)
            pari_t = pari(target_fp)
            
            private_key = int(pari.znlog(pari_t, pari_g, pari_p))
            print(f"[{method_name}] ✅ Found private key: {private_key}")
            
            # Quick verification
            if self.quick_verify(private_key, target_public_key):
                print(f"[{method_name}] ✅ Verification successful!")
                return private_key
        except Exception as e:
            print(f"[{method_name}] ❌ PARI/GP failed: {e}")
        
        return None
    
    def baby_step_giant_step_optimized(self, generator, target, limit):
        """Optimized baby-step giant-step algorithm."""
        m = int(limit**0.5) + 1
        
        # Baby steps with early termination
        baby_steps = {}
        current = 1
        
        for j in range(m):
            if current == target:
                return j
            baby_steps[current] = j
            current = (current * generator) % self.p
            
            # Early termination check
            if len(baby_steps) % 10000 == 0 and self.results:
                return None
        
        # Giant steps with early termination
        gamma = pow(generator, -m, self.p)
        y = target
        
        for i in range(m):
            if y in baby_steps:
                return i * m + baby_steps[y]
            y = (y * gamma) % self.p
            
            # Early termination check
            if i % 10000 == 0 and self.results:
                return None
        
        return None
    
    def pollard_rho_optimized(self, generator, target, method_name="Pollard's rho"):
        """Optimized Pollard's rho for discrete log."""
        def f(x, a, b, order):
            if x % 3 == 0:
                return (x * x) % self.p, (2 * a) % order, (2 * b) % order
            elif x % 3 == 1:
                return (x * generator) % self.p, (a + 1) % order, b
            else:
                return (x * target) % self.p, a, (b + 1) % order
        
        # Use pre-computed order
        order = p_minus_1
        
        x1, a1, b1 = 1, 0, 0
        x2, a2, b2 = 1, 0, 0
        
        # Reduced iteration limit for faster execution
        max_iterations = min(5000000, order)
        
        for i in range(max_iterations):
            x1, a1, b1 = f(x1, a1, b1, order)
            x2, a2, b2 = f(*f(x2, a2, b2, order), order)
            
            if x1 == x2:
                r = (a1 - a2) % order
                s = (b2 - b1) % order
                
                if s == 0:
                    continue
                
                try:
                    private_key = (r * pow(s, -1, order)) % order
                    return private_key
                except:
                    continue
            
            # Early termination check
            if i % 50000 == 0:
                if self.results:
                    return None
                print(f"[{method_name}] ... {i} iterations completed")
        
        return None
    
    def quick_verify(self, private_key, target_public_key):
        """Quick verification using 𝔽ₚ* mapping instead of full point multiplication."""
        try:
            # Compute expected target in 𝔽ₚ*
            expected = pow(self.generator_fp, private_key, self.p)
            
            # Get actual target
            if target_public_key == alice_public:
                actual = self.alice_fp
            elif target_public_key == bob_public:
                actual = self.bob_fp
            else:
                actual = self.conic_to_fp_star(target_public_key)
            
            return expected == actual
        except:
            return False
    
    def run_method_parallel(self, method_func, target_public_key, method_name):
        """Run a single method in parallel and store result."""
        try:
            result = method_func(target_public_key, method_name)
            if result is not None:
                self.results[method_name] = result
                print(f"[{method_name}] 🎉 SUCCESS! Private key: {result}")
            else:
                print(f"[{method_name}] ❌ Failed to find private key")
        except Exception as e:
            print(f"[{method_name}] 💥 Exception: {e}")
    
    def recover_private_key_parallel(self, target_public_key, target_name):
        """Run all methods in parallel to recover private key."""
        print(f"\n🎯 PARALLEL ATTACK ON {target_name.upper()}'S PRIVATE KEY")
        print("=" * 80)
        
        # Optimized method order: fastest first
        methods = [
            (self.recover_private_key_method_3, "SymPy"),  # Often fastest
            (self.recover_private_key_method_4, "PARI/GP"),  # Powerful backup
            (self.recover_private_key_method_1, "Baby-step giant-step"),  # Reliable
            (self.recover_private_key_method_2, "Pollard's rho"),  # Probabilistic
        ]
        
        # Run all methods in parallel
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submit all tasks
            futures = []
            for method_func, method_name in methods:
                future = executor.submit(self.run_method_parallel, method_func, target_public_key, method_name)
                futures.append(future)
            
            # Wait for first success or all to complete
            start_time = time.time()
            timeout = 180  # Reduced timeout to 3 minutes
            
            for future in as_completed(futures, timeout=timeout):
                if self.results:  # If any method succeeded
                    print(f"\n🎊 FIRST SUCCESSFUL METHOD COMPLETED!")
                    print(f"⏱️  Time taken: {time.time() - start_time:.2f} seconds")
                    
                    # Cancel remaining tasks
                    for f in futures:
                        f.cancel()
                    break
                
                try:
                    future.result(timeout=1)  # Check if completed
                except:
                    pass
            
            # If no success yet, wait for all to complete
            if not self.results:
                print(f"\n⏳ Waiting for all methods to complete...")
                for future in futures:
                    try:
                        future.result()
                    except Exception as e:
                        print(f"Method failed: {e}")
        
        # Return the first successful result
        if self.results:
            method_name, private_key = next(iter(self.results.items()))
            print(f"\n🎊 {target_name.upper()}'S PRIVATE KEY RECOVERED: {private_key}")
            print(f"✅ Method used: {method_name}")
            return private_key
        
        return None
    
    def decrypt_flag(self, private_key, encrypted_data, peer_public_key):
        """Decrypt the flag using recovered private key."""
        print(f"\n🔓 DECRYPTING FLAG")
        print("=" * 50)
        
        # Compute shared secret
        print("Computing shared secret...")
        shared_point = self.point_scalar_mult(private_key, peer_public_key)
        shared_x = shared_point[0]
        
        print(f"Shared secret (x-coordinate): {shared_x}")
        
        # Derive AES key
        key_material = hashlib.sha1(str(shared_x).encode()).digest()
        aes_key = key_material[:16]
        
        print(f"Derived AES key: {aes_key.hex()}")
        
        # Decrypt
        iv = bytes.fromhex(encrypted_data['iv'])
        ciphertext = bytes.fromhex(encrypted_data['encrypted_flag'])
        
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(ciphertext)
        
        try:
            decrypted = unpad(decrypted_padded, 16)
            flag = decrypted.decode('utf-8')
            print(f"\n🎉 FLAG RECOVERED: {flag}")
            return flag
        except Exception as e:
            print(f"❌ Decryption/unpadding failed: {e}")
            print(f"Raw decrypted (hex): {decrypted_padded.hex()}")
            return None


def main():
    """Main exploitation routine for the real challenge."""
    
    print("🚨 REAL FLAG RECOVERY EXPLOIT - OPTIMIZED PARALLEL VERSION")
    print("=" * 80)
    
    exploit = RealFlagExploit(p, D, G)
    
    print(f"\n📋 CHALLENGE DATA:")
    print(f"Alice's public key: {alice_public}")
    print(f"Bob's public key: {bob_public}")
    print(f"Encrypted flag IV: {encrypted_data['iv']}")
    print(f"Encrypted flag: {encrypted_data['encrypted_flag']}")
    
    # Try to recover Alice's private key first using parallel methods
    alice_private = exploit.recover_private_key_parallel(alice_public, "Alice")
    
    if alice_private is not None:
        # Decrypt flag using Alice's key and Bob's public key
        flag = exploit.decrypt_flag(alice_private, encrypted_data, bob_public)
        
        if flag:
            return
    
    # If Alice's key recovery failed, try Bob's key
    print(f"\n🔄 Trying Bob's private key...")
    exploit.results = {}  # Reset results for Bob
    
    bob_private = exploit.recover_private_key_parallel(bob_public, "Bob")
    
    if bob_private is not None:
        # Decrypt flag using Bob's key and Alice's public key
        flag = exploit.decrypt_flag(bob_private, encrypted_data, alice_public)
        
        if flag:
            return
    
    print("\n💥 EXPLOITATION FAILED")
    print("All parallel methods failed to recover private keys.")
    print("The discrete log problem might be harder than expected.")
    print("Consider using more sophisticated algorithms or distributed computing.")


if __name__ == "__main__":
    main()