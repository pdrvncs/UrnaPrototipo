class Cipher:

    def __init__(self, c1, c2):
        self.c1 = c1
        self.c2 = c2

    def __str__(self):
        # s = 'Mensagem cifrada ' + '\n'
        s = ''
        s += '(' + str(self.c1)
        s += ', ' + str(self.c2) + ')'
        return s

def multiply(cifra1, cifra2, key):

    '''Recebe duas cifras e uma chave, retorna uma nova cifra c3 = c1 * c2 '''

    if isinstance(cifra1, Cipher) and cifra2 is None:
        return cifra1
    if isinstance(cifra2, Cipher) and cifra1 is None:
        return cifra2
    if isinstance(cifra1, Cipher) and isinstance(cifra2, Cipher):
        return Cipher((cifra1.c1 * cifra2.c1) % key.p, (cifra1.c2 * cifra2.c2) % key.p)

    print('Erro ao multiplicar cifras ' + str(cifra1) + ' ' + str(cifra2))
    return None
