# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 14:10:38 2022

@author: Daria
"""


def ROLT(x, r):
    return ((x << r)%(1 << s)|(x >> (s - r)))


def h(p):
    p[0] = (p[0] + p[1])%(1 << s)
    p[3] ^= p[0]
    p[3]= ROLT(p[3], r[0])
    p[2] = (p[2] + p[3])%(1 << s)
    p[1] ^= p[2]
    p[1] = ROLT(p[1], r[1])
    p[0] = (p[0] + p[1])%(1 << s)
    p[3] ^= p[0]
    p[3] = ROLT(p[3], r[2])
    p[2] = (p[2] + p[3])%(1 << s)
    p[1] ^= p[2]
    p[1] = ROLT(p[1], r[3])
    return p


def gen_key_sigma(key, st = [0, 0, 0, 1]):
    key_l, key_r = key[:4], key[4:]
    st = [(st[i] + key_l[i])%(1 << s) for i in range(4)]
    st = h(h(st))
    st = [st[i] ^ key_r[i] for i in range(4)]
    st = h(h(st))
    st = [(st[i] + key_l[i])%(1 << s) for i in range(4)]
    return h(h(st))


def gen_round_keys(key, sigma, tmv):
    round_keys = []
    for j in range(t):
        st = key[:4] if j%2 == 0 else key[4:]
        key_t = [(sigma[i] + tmv[i])%(1 << s) for i in range(4)]
        st = [(st[i] + key_t[i])%(1 << s) for i in range(4)]
        st = h(h(st))
        st = [st[i] ^ key_t[i] for i in range(4)]
        st = h(h(st))
        st = [(st[i] + key_t[i])%(1 << s) for i in range(4)]
        round_keys.append(st)
        tmv = [tmv[i] << 1 for i in range(4)]
        if j%2 == 1:
            key = key[1:] + key[:1]
    return round_keys


def cipher(plain_text):
    L, R = plain_text[:4], plain_text[4:]
    for j in range(t):
        L_next = h(h([L[i] ^ ROUND_KEYS[j][i] for i in range(4)]))
        L_next = [R[i] ^ L_next[i] for i in range(4)]
        R, L = L, L_next
    return L + R


def decipher(cipher_text):
    R, L = cipher_text[:4],  cipher_text[4:]
    for j in reversed(range(t)):
        L_next = h(h([L[i] ^ ROUND_KEYS[j][i] for i in range(4)]))
        L_next = [R[i] ^ L_next[i] for i in range(4)]
        R, L = L,  L_next
    return  R + L


if __name__ == '__main__':
    #file = open('plaintext512.txt', 'r')
    file = open('plaintext256.txt', 'r')
    data = file.readlines()
    master_key = [int(k, 16) for k in data[0].split()]
    plaintext = [int(p, 16) for p in data[1].split()]
    file.close()
    if master_key[0].bit_length() < 32:
        s, t, r, TMV = 32, 10, [16, 12, 8, 7], [0x000F000F]*4
    else:
        s, t, r, TMV = 64, 14, [32, 24, 16, 15], [0x000F000F000F000F]*4
    ROUND_KEYS = gen_round_keys(master_key, gen_key_sigma(master_key), TMV)
    ciphertext = cipher(plaintext)
    print('Ciphertext:\n')
    print([hex(c).upper() for c in ciphertext])



