# Roll ur own Solution

Edit: This renders perfectly fine in Obsidian.md, idk why github does this shit. sorry but am not fixing all the latex syntax errors, fuck it. 

- Author: [supasuge](https://github.com/supasuge)

## Challenge overview

In this challenge, let $N = p\,q$, where $p$ and $q$ are *safe primes*, i.e. $p = 2p' + 1$ and $q = 2q' + 1$ with $p',q'$ themselves prime.  
- [Source](https://en.wikipedia.org/wiki/Safe_and_Sophie_Germain_primes)

A *Sophie Germain prime* is a prime $p$ such that $2p + 1$ is also prime; the number $2p+1$ is then called a *safe prime*. Sophie Germain discovered this theorem while trying to prove Fermat's Last Theorem.
One early attempt by Sophie Germain to prove Fermat’s Last Theorem was to let $p$ be a prime of the form $8k+7$ and take $n = p-1$.  In that case  

$x^n + y^n = z^n$

is unsolvable.  Although her proof remained unfinished, she proved what is now called *Germain’s Theorem*: if $p$ is an odd prime and $2p+1$ is also prime, then any solution to  

$x^n + y^n = z^n,\quad n=p-1,$

must have $p\mid x$, $p\mid y$, or $p\mid z$, ruling out the “first case” of FLT for such primes.

---

## Number‐theoretic background on safe/Sophie Germain primes

1. **Sophie Germain prime**  
   A prime $p$ with $2p+1$ also prime.  
   _Examples:_ $p=11$ is Sophie Germain because $2\cdot11+1=23$ is prime.  
   Conjectured infinitely many exist, but unproven.

2. **Safe prime**  
   A prime $q$ such that $(q-1)/2$ is prime.  Equivalently, $q=2p+1$ for some Sophie Germain prime $p$.  
   Safe primes are prized in cryptography because the multiplicative group $(\mathbb Z/q\mathbb Z)^\times$ then has a large prime‐order subgroup of order $(q-1)/2$ .

3. **Applications in cryptography**  
   - Diffie–Hellman: choosing a safe‑prime modulus ensures the prime‐order subgroup is as large as possible relative to $q$.  
   - Pollard’s $p-1$ factoring method performs worst when $p-1$ and $q-1$ each have a large prime factor, as is the case for safe primes.

---

## Key algebraic properties

Let $p=2p'+1$, $q=2q'+1$.  Then

$$\varphi(N) = (p-1)(q-1) = 2p',\times 2q' = 4,p',q'$$

Choose a generator $g$ of the prime‑order subgroups modulo $p$ and $q$.  Because each safe prime’s multiplicative group is cyclic of order $2p'$ (resp.\ $2q'$), a primitive root $g$ satisfies

$$\text{ord}_p(g)  = 2p',\quad
\text{ord}_q(g) = 2q'.$$

By the Chinese Remainder Theorem, the order of $g$ modulo $N$ is

$$
\mathrm{lcm}(2p',2q') = 2\,p'\,q'
= \frac{\varphi(N)}{2}.
$$

---

## Oracle design and subgroup‐membership test

The remote “get_bit” oracle behaves as follows for bit index $0\le i<8\cdot32$:

```python
if FLAG_bit_i == 1:
    # returns a random element of ⟨g⟩
    return g^r mod N    # 2 ≤ r < φ(N)
else:
    # returns a uniformly random residue mod N
    return random x ∈ [1,N−1]
````

* Any $x \in \langle g \rangle$ satisfies $x^{\varphi(N)/2}\equiv1\pmod N$.
* A uniformly random $x\notin\langle g\rangle$ will, with overwhelming probability, satisfy $x^{\varphi(N)/2}\equiv -1\pmod N$, since $(\mathbb Z/N)^\times/\langle g\rangle$ has order 2.

Thus the **bit‐recovery test** is simply:

```python
# φ_half = φ(N)//2 = 2·p'·q'
bit = 1 if pow(x, φ_half, N) == 1 else 0
```

Each query leaks exactly one bit of the flag.

---

## Putting it all together

1. **Compute** $\varphi(N)/2 = 2p'q'$.
2. **For** $i=0$ to $255$:

* Send `{"option":"get_bit","i":"i"}`
* Parse the hex response $x$.
* Compute $x^{\varphi(N)/2}\bmod N$.
* Record bit = $1$ if result = $1$, else $0$.

3. **Reassemble** the 256 bits into 32 bytes (little‑endian within each byte) to recover the ASCII flag.

This runs in $O(256)$ oracle calls plus $O(256)$ modular exponentiations—easily done in a second or two in Python.

---

## References

* Definition of Sophie Germain and safe primes 
* Cryptographic use and Pollard’s $p-1$ consideration for safe primes 
* Chinese Remainder Theorem and lcm‐order argument (standard group‐theory)
