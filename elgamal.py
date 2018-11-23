import random
from cipher import Cipher
from keys import PrivateKey, PublicKey
from modular import modular_inverse

def elgamal_encrypt(publicKey, m):

    if not isinstance(publicKey, PublicKey):
        print('Chave publica invalida')
        return None

    if m >= publicKey.p:
        print ('Mensagem invalida (m > p)')
        return None

    s = random.randint(1, publicKey.p - 2)

    c1 = pow(publicKey.g, s, publicKey.p)  # g^k mod p
    c2 = (m % publicKey.p) * pow(publicKey.beta, s, publicKey.p)
    c = Cipher(c1, c2)

    return c


def elgamal_decrypt(cifra, publicKey, privateKey):

    if isinstance(cifra, Cipher) is False:
        print ('Mensagem cifrada invalida')
        return None

    if isinstance(privateKey, PrivateKey) is False:
        print ('Chave privada invalida')
        return None

    s = pow(cifra.c1, privateKey.x, publicKey.p)
    a = modular_inverse(s, publicKey.p)
    return (a * cifra.c2) % publicKey.p
