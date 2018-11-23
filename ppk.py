import random
from os import urandom
import hashlib
from modular import modular_inverse

class PPK_Prova:

    def xor(self, a, b):
        return [bin((int(x,2) ^ int(y,2)))[2:].zfill(8) for x,y in zip(a,b)]

    def str2binarray(self, s):
        return [bin(ord(ch))[2:].zfill(8) for ch in s ]

    def bin2dec(self, s):
        return int(''.join([str(int(x,2)) for x in s]))

    def hash2bin(self, s):
        return self.str2binarray(s)

    def hash2number(self, s):
        x = self.str2binarray(s)
        return int(''.join([str(int(y,10)) for y in x]), 2)

    def __init__(self, cifra, publicKey, s, m1, m2):
        self.cifra = cifra
        p, g = publicKey.p, publicKey.g

        t = random.randint(1, p - 2)
        self.s2 = random.randint(1, p - 2)
        self.v2 = random.randint(1, p - 2)
        self.t0 = pow(g, t, p)
        self.t1 = pow(publicKey.beta, t, p)
        t2a = pow(g, m2 * self.v2, p)
        t2b = pow(publicKey.beta, self.s2, p)
        t2c = pow(modular_inverse(cifra.c2, p), self.v2, p) % p
        self.t2 = (t2a * t2b * t2c) % p
        v = int(hashlib.sha224(str(self.cifra.c1).encode('utf-8') + str(self.cifra.c2).encode('utf-8') + str(self.t0).encode('utf-8') + str(self.t1).encode('utf-8') + str(self.t2).encode('utf-8')).hexdigest(),16)    
        self.v1 = v ^ self.v2
        self.s1 = s * self.v1 + t

    def __str__(self):
        s =  '     cifra  : ' + str(self.cifra) + '\n'
        s += '     t0     : ' + str(self.t0) + '\n'
        s += '     t1     : ' + str(self.t1) + '\n'
        s += '     t2     : ' + str(self.t2) + '\n'
        s += '     v1     : ' + str(self.v1) + '\n'
        s += '     v2     : ' + str(self.v2) + '\n'
        s += '     s1     : ' + str(self.s1) + '\n'
        s += '     s2     : ' + str(self.s2) + '\n'
        return s


def ppk_verifica(ppkProva, publicKey, m1, m2):
    p = publicKey.p
    g = publicKey.g
    if not isinstance(ppkProva, PPK_Prova):
        print('Prova invalida')
        return None
    # teste 1
    v = int(hashlib.sha224(str(ppkProva.cifra.c1).encode('utf-8') + str(ppkProva.cifra.c2).encode('utf-8') + str(ppkProva.t0).encode('utf-8') + str(ppkProva.t1).encode('utf-8') + str(ppkProva.t2).encode('utf-8')).hexdigest(),16)
    if v != ppkProva.v1 ^ ppkProva.v2:
        print('Teste 1 Falhou... v != v1 ^ v2')
        print('Hash computado :' + str(v))
        print('v1 recebido: ' + str(ppkProva.v1))
        print('v2 recebido: ' + str(ppkProva.v2))
        return False

    # teste 2
    a = pow(publicKey.g, ppkProva.s1, p)
    b = ((ppkProva.t0 % p) * pow(ppkProva.cifra.c1, ppkProva.v1, p)) % p
    if a != b:
        print('Teste 2 Falhou...')
        print(str(a) + ' != ' + str(b))
        return False

    # teste 3
    a = pow(publicKey.beta, ppkProva.s1, p)
    ba = ppkProva.t1 % p
    bb = ppkProva.cifra.c2 % p
    bc = pow(modular_inverse(g, p), m1, p) % p
    b = (ba * pow(bb * bc, ppkProva.v1, p)) % p
    if a != b:
        print('Teste 3 Falhou...')
        print(str(a) + ' != ' + str(b))
        return False

    # teste 4
    a = pow(publicKey.beta, ppkProva.s2, p)
    ba = ppkProva.t2 % p
    bb = ppkProva.cifra.c2 % p
    bc = pow(modular_inverse(g, p), m2, p) % p
    b = (ba * pow(bb * bc, ppkProva.v2, p)) % p
    if a != b:
        print('Teste 4 Falhou...')
        print(str(a) + ' != ' + str(b))
        return False

    return True
        
