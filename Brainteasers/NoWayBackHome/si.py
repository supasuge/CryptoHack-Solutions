from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes, inverse
from hashlib import sha256

# Given from the challenge (replace these with actual given values):
p = 10699940648196411028170713430726559470427113689721202803392638457920771439452897032229838317321639599506283870585924807089941510579727013041135771337631951
q = 11956676387836512151480744979869173960415735990945471431153245263360714040288733895951317727355037104240049869019766679351362643879028085294045007143623763

# Derived modulus
n = p * q

vka = 124641741967121300068241280971408306625050636261192655845274494695382484894973990899018981438824398885984003880665335336872849819983045790478166909381968949910717906136475842568208640203811766079825364974168541198988879036997489130022151352858776555178444457677074095521488219905950926757695656018450299948207
vkakb = 114778245184091677576134046724609868204771151111446457870524843414356897479473739627212552495413311985409829523700919603502616667323311977056345059189257932050632105761365449853358722065048852091755612586569454771946427631498462394616623706064561443106503673008210435922340001958432623802886222040403262923652
vkb = 6568897840127713147382345832798645667110237168011335640630440006583923102503659273104899584827637961921428677335180620421654712000512310008036693022785945317428066257236409339677041133038317088022368203160674699948914222030034711433252914821805540365972835274052062305301998463475108156010447054013166491083
c_hex = 'fef29e5ff72f28160027959474fc462e2a9e0b2d84b1508f7bd0e270bc98fac942e1402aa12db6e6a36fb380e7b53323'

# Step 1: Compute the "primed" values by dividing by p
vka_prime = vka // p
vkakb_prime = vkakb // p
vkb_prime = vkb // p

# All arithmetic now considered modulo q
modulus = q

# Step 2: Solve for k_A and k_B
# k_B = (vkakb_prime * inverse(vka_prime, q)) mod q
inv_vka_prime = inverse(vka_prime, modulus)
k_B = (vkakb_prime * inv_vka_prime) % modulus

# k_A = (vkakb_prime * inverse(vkb_prime, q)) mod q
inv_vkb_prime = inverse(vkb_prime, modulus)
k_A = (vkakb_prime * inv_vkb_prime) % modulus

# Step 3: Solve for r
# vka_prime = r * k_A mod q  =>  r = vka_prime * k_A^{-1} mod q
inv_k_A = inverse(k_A, modulus)
r = (vka_prime * inv_k_A) % modulus

# Step 4: Compute v = p * r
v = p * r

# Step 5: Derive the AES key
key = sha256(long_to_bytes(v)).digest()

# Step 6: Decrypt the ciphertext
c_bytes = bytes.fromhex(c_hex)
cipher = AES.new(key, AES.MODE_ECB)
decrypted = cipher.decrypt(c_bytes)

# The message is padded (PKCS#7), unpad it:
# AES block size is 16 bytes
from Crypto.Util.Padding import unpad
flag = unpad(decrypted, 16)

print(flag)  # Should print the flag: crypto{...}
