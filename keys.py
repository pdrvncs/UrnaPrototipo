import random
from modular import generate_large_prime, find_primitive_root


class PublicKey:
    '''
    Classe que representa uma chave publica (p, g, beta)
    '''
    def __init__(self, p, g, beta):
        self.p = p
        self.g = g
        self.beta = beta

    def __str__(self):
        return  'Chave publica (p, g, beta)  -> ' + '(' + str(self.p) + ', ' + str(self.g) + ', ' + str(self.beta) + ')'
       

class PrivateKey:
    '''
    Classe que representa uma chave privada (x)
    '''
    def __init__(self, x):
        self.x = x

    def __str__(self):
        return  'Chave privada -> ' + str(self.x)

def gera_par_de_chaves(bits = 8):
    '''
    Retorna um dicionario contendo 'publicKey': uma instancia PublicKey e 'privateKey': uma instancia de PrivateKey
    As duas chaves sao de tamanho bits bits
    '''
    p = generate_large_prime(bits)
    g = find_primitive_root(p)
    x = random.randint(1, p - 2) 

    publicKey = PublicKey(p, g, pow(g, x, p))
    privateKey = PrivateKey(x)

    return {'publicKey': publicKey, 'privateKey': privateKey}
