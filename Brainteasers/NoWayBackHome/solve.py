from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from hashlib import sha256
from Crypto.Util.number import bytes_to_long, long_to_bytes

def recover_v():
    p = 10699940648196411028170713430726559470427113689721202803392638457920771439452897032229838317321639599506283870585924807089941510579727013041135771337631951
    q = 11956676387836512151480744979869173960415735990945471431153245263360714040288733895951317727355037104240049869019766679351362643879028085294045007143623763
    n = p * q
    vka = 124641741967121300068241280971408306625050636261192655845274494695382484894973990899018981438824398885984003880665335336872849819983045790478166909381968949910717906136475842568208640203811766079825364974168541198988879036997489130022151352858776555178444457677074095521488219905950926757695656018450299948207
    
    # Since vka ≡ 0 (mod p), we can recover r * k_A by dividing vka by p
    r_ka = vka // p
    
    # Now we know v = p * r where r = r_ka/k_A
    # Try small divisors of r_ka as potential values for k_A
    potential_rs = []
    for i in range(1, 1000):
        if r_ka % i == 0:
            potential_rs.append(r_ka // i)
    
    # Try each potential v value
    c = 'fef29e5ff72f28160027959474fc462e2a9e0b2d84b1508f7bd0e270bc98fac942e1402aa12db6e6a36fb380e7b53323'
    for r in potential_rs:
        v = (p * r) % n
        key = sha256(long_to_bytes(v)).digest()
        cipher = AES.new(key, AES.MODE_ECB)
        try:
            pt = unpad(cipher.decrypt(bytes.fromhex(c)), 16)
            if pt.startswith(b'crypto{'):
                return pt
        except:
            continue
    return None

print(recover_v())
