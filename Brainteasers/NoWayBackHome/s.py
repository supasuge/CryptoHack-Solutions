from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from hashlib import sha256
from Crypto.Util.number import long_to_bytes

def solve():
    # Given values
    p = 10699940648196411028170713430726559470427113689721202803392638457920771439452897032229838317321639599506283870585924807089941510579727013041135771337631951
    vka = 124641741967121300068241280971408306625050636261192655845274494695382484894973990899018981438824398885984003880665335336872849819983045790478166909381968949910717906136475842568208640203811766079825364974168541198988879036997489130022151352858776555178444457677074095521488219905950926757695656018450299948207
    c = 'fef29e5ff72f28160027959474fc462e2a9e0b2d84b1508f7bd0e270bc98fac942e1402aa12db6e6a36fb380e7b53323'

    # Since vka = (v * k_A) mod n and v = (p * r) mod n
    # Then vka is also a multiple of p
    # We can recover (r * k_A) by dividing vka by p
    r_ka = vka // p
    
    # Now v = p * r, where r is r_ka / k_A
    v = p * (r_ka // p)  # This should give us v
    
    # Get AES key
    key = sha256(long_to_bytes(v)).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(bytes.fromhex(c))
    return plaintext

print(solve())