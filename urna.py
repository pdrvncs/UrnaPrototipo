from voto import Voto, VotoElemento
import random
from elgamal import elgamal_encrypt
from elgamal_exp import elgamalexp_encrypt
from bitcom import bit_commitment
from ppk import PPK_Prova
from cipher import multiply
import hashlib

class Urna:
    '''
    Classe que simula uma urna. A urna deve receber uma copia da chave publica (para
    realizar a encriptação) e a lista de candidatos (para exibir as informações e verificar
    o número inserido pelo eleitor).
    '''
    def __init__(self, publicKey, candidatos):
        '''
        publicKey   : a chave publica
        candidatos  : a lista de candidatos
        '''
        self.publicKey = publicKey
        self.candidatos = candidatos

    def codifica_voto(self, numeroCandidato):
        votoCodificado = []
        for c in self.candidatos:
            if c.numero == numeroCandidato:
                votoCodificado.append(2)
            else:
                votoCodificado.append(1)
        return votoCodificado

    def vota(self, idEleitor, numeroCandidato):
        '''
        Função que simula o momento que o eleitor vota. O eleitor (idEleitor) entra
        com o candidato escolhido (numeroCandidato) e a máquina gera uma instancia
        da classe Voto e envia para o Counter.

        idEleitor       : a identificação do eleitor
        numeroCandidato : o numero do candidato escolhido pelo eleitor

        '''
        votoCodificado = self.codifica_voto(numeroCandidato)
        vetor = []
        PPK_Y = None
        h = None

        vetor_soma = None
        s_soma = 0
        # print('Voto codificado: ' + str(votoCodificado))
        voto_nulo = True
        for a in votoCodificado:
            if a == 2:
                voto_nulo = False

            s = random.randint(1, self.publicKey.p - 2)         
            s_soma += s
            c = elgamalexp_encrypt(self.publicKey, a, s)
            s_cifrado = elgamal_encrypt(self.publicKey, s)
            bitcom = bit_commitment(a, s, self.publicKey)
            if a == 1:
                ppk = PPK_Prova(c, self.publicKey, s, 1, 2)
            else:
                c_alt = elgamalexp_encrypt(self.publicKey, 1, s)
                ppk = PPK_Prova(c_alt, self.publicKey, s, 1, 2)
            
            voto = VotoElemento(c, s_cifrado, bitcom, ppk)
            vetor.append(voto)

            vetor_soma = multiply(vetor_soma, c, self.publicKey)

        if voto_nulo is True:
            PPK_Y = PPK_Prova(vetor_soma, self.publicKey, s_soma, len(votoCodificado), len(votoCodificado) + 1)
        else:
            cifra_alt = elgamalexp_encrypt(self.publicKey, len(votoCodificado), s_soma)
            PPK_Y = PPK_Prova(cifra_alt, self.publicKey, s_soma, len(votoCodificado), len(votoCodificado) + 1)
        
            h = hashlib.sha224(str(vetor).encode('utf-8')).hexdigest()

        return Voto(idEleitor, vetor, PPK_Y, h)



