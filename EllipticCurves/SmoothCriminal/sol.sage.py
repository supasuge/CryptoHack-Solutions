

# This file was *autogenerated* from the file sol.sage
from sage.all_cmdline import *   # import sage library

_sage_const_1 = Integer(1); _sage_const_0 = Integer(0); _sage_const_16 = Integer(16); _sage_const_310717010502520989590157367261876774703 = Integer(310717010502520989590157367261876774703); _sage_const_2 = Integer(2); _sage_const_3 = Integer(3); _sage_const_179210853392303317793440285562762725654 = Integer(179210853392303317793440285562762725654); _sage_const_105268671499942631758568591033409611165 = Integer(105268671499942631758568591033409611165); _sage_const_272640099140026426377756188075937988094 = Integer(272640099140026426377756188075937988094); _sage_const_51062462309521034358726608268084433317 = Integer(51062462309521034358726608268084433317); _sage_const_280810182131414898730378982766101210916 = Integer(280810182131414898730378982766101210916); _sage_const_291506490768054478159835604632710368904 = Integer(291506490768054478159835604632710368904)
from Crypto.Hash import SHA1

from Crypto.Cipher import AES

from Crypto.Util.Padding import pad, unpad

import hashlib



def is_pkcs7_padded(message):

    padding = message[-message[-_sage_const_1 ]:]

    return all(padding[i] == len(padding) for i in range(_sage_const_0 , len(padding)))



def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):

    # Derive AES key from shared secret

    sha1 = hashlib.sha1()

    sha1.update(str(shared_secret).encode('ascii'))

    key = sha1.digest()[:_sage_const_16 ]

    # Decrypt flag

    ciphertext = bytes.fromhex(ciphertext)

    iv = bytes.fromhex(iv)

    cipher = AES.new(key, AES.MODE_CBC, iv)

    plaintext = cipher.decrypt(ciphertext)


    if is_pkcs7_padded(plaintext):

        return unpad(plaintext, _sage_const_16 ).decode('ascii')

    else:

        return plaintext.decode('ascii')


p = _sage_const_310717010502520989590157367261876774703 

F = GF(p)

E = EllipticCurve(F, [_sage_const_2 , _sage_const_3 ])


g_x = _sage_const_179210853392303317793440285562762725654 

g_y = _sage_const_105268671499942631758568591033409611165 

G = E(g_x, g_y)


b_x = _sage_const_272640099140026426377756188075937988094 

b_y = _sage_const_51062462309521034358726608268084433317 

B = E(b_x, b_y)


public = E(_sage_const_280810182131414898730378982766101210916 , _sage_const_291506490768054478159835604632710368904 )


iv = '07e2628b590095a5e332d397b8a59aa7'

encrypted_flag = '8220b7c47b36777a737f5ef9caa2814cf20c1c1ef496ec21a9b4833da24a008d0870d3ac3a6ad80065c138a2ed6136af'


n = discrete_log(public, G, operation='+')

# n = 47836431801801373761601790722388100620

shared_secret = (B * n)[_sage_const_0 ]


print(decrypt_flag(shared_secret, iv, encrypted_flag))
