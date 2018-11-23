import random
from cipher import Cipher
from keys import PrivateKey, PublicKey
from modular import modular_inverse

def elgamalexp_encrypt(publicKey, m, s):

    if not isinstance(publicKey, PublicKey):
        print('Chave publica invalida')
        return None

    if m >= publicKey.p:
        print ('Mensagem invalida (m > p)')
        return None

    '''if m < 1:
        print ('Aviso m < 1')'''

    c1 = pow(publicKey.g, s, publicKey.p)  # g^k mod p
    c2 = pow(publicKey.g, m, publicKey.p) * pow(publicKey.beta, s, publicKey.p)
    c = Cipher(c1, c2)

    return c

def brute_force(m, g, p, maxValue):
    for x in range(1, maxValue):
        if pow(g, x, p) == m % p:
            return x
    print('Forca bruta nao conseguiu resolver a equacao ' + str(g) + '^' + str(m) + ' = ' + str(m) + " mod " + str(p))
    return None

def elgamalexp_decrypt(cifra, publicKey, privateKey, maxValue=0):
    if maxValue == 0:
        maxValue = privateKey.p

    if isinstance(cifra, Cipher) is False:
        print ('Mensagem cifrada invalida')
        return None

    if isinstance(privateKey, PrivateKey) is False:
        print ('Chave privada invalida: ' + type(privateKey))
        return None

    s2 = (cifra.c2 * pow(modular_inverse(cifra.c1, publicKey.p), privateKey.x, publicKey.p)) % publicKey.p  # encontra g^m = s2 mod p'''

    return brute_force(s2, publicKey.g, publicKey.p, maxValue)  # resolve a equacao acima para m usando forca bruta



