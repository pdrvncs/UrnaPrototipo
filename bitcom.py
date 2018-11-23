from keys import PublicKey
from modular import modular_inverse


def bit_commitment(m, s, publicKey):
    if not isinstance(publicKey, PublicKey):
        print('Chave publica invalida')
        return None

    if m >= publicKey.p:
        print ('Mensagem invalida (m > p)')
        return None

    if s >= publicKey.p - 2:
        print ('S invalido ')
        return None

    return pow(publicKey.g, s, publicKey.p) * pow(publicKey.beta, m, publicKey.p)

