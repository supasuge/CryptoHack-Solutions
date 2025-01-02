# Everything is Still Big (CryptoHack - RSA)

The code snippet in `src.py` is the challenge code from CryptoHack. In this challenge, two large primes $p$ and $q$, each $1024$ bits. The vulnerability in this challenges arises from:

```python
while True:
        d = getrandbits(512)
        if (3*d)**4 > N and gcd(d,phi) == 1:
            e = inverse(d, phi)
            break
```

$$
(3d)^4 > N 
\Longrightarrow
81\,d^4 > N
\Longrightarrow
d > \sqrt[4]{\frac{N}{81}}
\approx\
\frac{N^{\tfrac14}}{3}.
$$

Although the number certainly is isn't tiny, $d$ is significantly smaller than half the size of $\phi(N)$ that would expect with a random RSA key.

Boneh and durfee's attack only works if $d < N^{\beta}$ for some $\beta < 0.292$, the relationship between $e$, $d$, and $\Phi(N)$ can be transformed into a bivariate polynomial equation:

$$
e \cdot d - k \cdot \Phi(N) = 1,
$$

where $k$ is an unknown integer.

## Solution code

The solution code is from written by [David Wong](https://github.com/mimoo), a well known cryptographer. He has some very good blog posts, books, and youtube videos explaining various attacks on RSA and other cryptographic problems.

[Here is the original source code](https://github.com/mimoo/RSA-and-LLL-attacks/blob/master/boneh_durfee.sage), I simply added in the parameters $N$, $e$, and $C$ then added a bit of code to properly convert the output to a readable form. [Source](./boneh_durfee.sage)

### Resources provided from the challenge

- [20 years of attacks on RSA - Dan Boneh](https://crypto.stanford.edu/~dabo/papers/RSA-survey.pdf)

#### Additional Resources

- [Lattice based attacks on RSA](https://github.com/mimoo/RSA-and-LLL-attacks/tree/master?tab=readme-ov-file#boneh-durfee)
    - [YouTube Video](https://www.youtube.com/watch?v=3cicTG3zeVQ   )
- [Boneh and Durfee's paper](https://crypto.stanford.edu/~dabo/papers/RSA-survey.pdf)
