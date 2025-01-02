order = 6277101735386680763835789423176059013767194773182842284081 

r1 = 0xa37abc6c431f9ac398bf5bd1aa6678320ace8ecb93d23f2a

s1 = 0xc3ddfa6bca8ad15a72d8ca32a5a576155da4ddaa43b1f0aa

s1_inv = inverse_mod(s1, order)

z1 = 236894979676116967369153264540878706747091303513

r2 = 0x2fa1f92d1ecce92014771993cc14899d4b5977883397edde

s2 = 0x7d86b77b5d1d45ebaf226a52d77a62f7afbaafa80c002961

s2_inv = inverse_mod(s2, order)

z2 = 873865316854725788202849324608451680951850980105


matrix = [[order, 0, 0, 0], [0, order, 0, 0],

[r1*s1_inv, r2*s2_inv, (2^96) / order, 0],

[z1*s1_inv, z2*s2_inv, 0, 2^96]]

sol = Matrix(matrix).LLL()

r1_inv = inverse_mod(r1, order)

row = sol[2]

potential_nonce_1 = (row[0])%order

potential_priv_key = (r1_inv * ((potential_nonce_1 * s1) - z1))%order

print("the secret is: ",potential_priv_key)