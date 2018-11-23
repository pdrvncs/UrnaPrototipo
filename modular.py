import random


def miller_rabin(n, k):
    ''' 
    teste de primalidade de Miller-Rabin
    https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Primality_Testing 
    '''
    if n % 2 == 0:
        return False
    s = 0
    d = n - 1
    while d % 2 == 0:
        s = s + 1
        d = d >> 1

    for i in range(0, k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for j in range(1, s):
            x = pow(x, 2, n)
            if x == 1:
                return False
            if x == n - 1:
                continue
        return False
    return True


def generate_large_prime(bits=8):
    primeCandidate = random.getrandbits(bits)
    if(primeCandidate % 2 == 0):
        primeCandidate += 1

    while miller_rabin(primeCandidate, 64) is False:
        primeCandidate += 2

    return primeCandidate


def find_primitive_root(p):
    '''
    Encontra raiz primitiva. 
    Fonte: https://github.com/RyanRiddle/elgamal/blob/master/elgamal.py
    '''
    if p == 2:
        return 1
    # the prime divisors of p-1 are 2 and (p-1)/2 because
    # p = 2x + 1 where x is a prime
    p1 = 2
    p2 = (p - 1) // p1

    # test random g's until one is found that is a primitive root mod p
    while(1):
        g = random.randint(2, p - 1)
        # g is a primitive root if for all prime factors of p-1, p[i]
        # g^((p-1)/p[i]) (mod p) is not congruent to 1
        if not (pow(g, (p - 1) // p1, p) == 1):
            if not pow(g, (p - 1) // p2, p) == 1:
                return g

def modular_inverse(a, p):
    u, v, x1, x2 = a, p, 1, 0
    while u != 1:
        # print(u)
        q = v // u
        r = v - q * u
        x = x2 - q * x1
        v = u
        u = r
        x2 = x1
        x1 = x
    return x1 % p