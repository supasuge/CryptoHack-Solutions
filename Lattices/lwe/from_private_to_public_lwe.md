# From private to public LWE

**Question**: This can be turned into a public key cryptosystem by using the "additively homomorphic" property of LWE. That is, given an encryption $⟨A,b⟩$ encrypting the number mm, it is possible for anyone to turn this into a valid encryption of m+m2m+m2​ for any number m2m2​. Explicitly, this is done by computing $⟨A,b+m2⟩$ for low-bit messages (high-bit noise) and $⟨A,b+\Delta⋅m2​⟩$ for high-bit messages (low-bit noise).

While this additively homomorphic property is more straightforward to see when the message is stored in low-bits, it is also present when the message is stored in high-bits.

Similarly, adding two LWE ciphertexts produces a new valid ciphertext which encrypts the sum of the corresponding plaintexts. The owner of the private key can use this property to turn LWE into a public-key system by releasing many different "encryptions of zero" as the public key. For Alice to use this information to encrypt, she first chooses a random subset of these "encryptions of zero" and add them together. By the second additively homomorphic property, this is also a valid encryption of zero. Next, Alice creates a new encoding of her message mm, and adds this encoded message to this new encryption of zero. By the first additively homomorphic property, this is a valid encryption of mm. This procedure requires the distribution from which the noise samples are drawn to be carefully chosen so that the final error term is (with high probability) below the threshold needed to decrypt.

In order for this to be secure, it must be hard for an adversary to determine which public key samples were summed to produce the LWE ciphertext. To ensure this, the number of "encryptions of zero" in the public key must be significantly larger than the LWE dimension. As such, the size of the public key scales as $O(n^{2}log⁡(q))$ bits, making LWE cryptosystems have large public keys.

What is the size of a Kyber1024 public key in bytes?

$$
\boxed{1,568}
$$

Source: https://medium.com/asecuritysite-when-bob-met-alice/goodbye-ecdh-and-hello-to-kyber-46415ef23d30