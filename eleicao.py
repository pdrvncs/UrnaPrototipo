import random

class Eleicao:
    '''
    Classe genérica que simula uma eleição completa. Uma eleição é basicamente composta de uma chave
    pública, uma chave privada, uma lista de eleitores e uma lista de candidatos. O Counter recebe 
    uma cópia completa da eleição enquanto cada urna recebe uma cópia da chave pública e da lista de 
    candidatos. A lista de eleitores é utilizada para verificar se um eleitor está regular.
    '''
    def __init__(self, publicKey, privateKey, eleitores, candidatos):
        self.publicKey = publicKey
        self.privateKey = privateKey
        self.eleitores = eleitores
        self.candidatos = candidatos
        self.Ncandidatos = len(self.candidatos)
        self.Neleitores = len(self.eleitores)

    def encontra_candidato(self, numeroCandidato):
        '''
        Retorna um Candidato na lista de candidatos pelo numero
        '''
        for t in self.candidatos:
            if numeroCandidato == t.numero:
                return t
        print ('Candidato de numero ' + str(numeroCandidato) + ' nao encontrado')
        return None

    def __str__(self):
        s = ''
        s += '- - - Eleicao - - - \n\n'
        s += str(self.Neleitores) + ' eleitores cadastrados \n'
        s += str(self.publicKey) + '\n'
        s += str(self.privateKey) + '\n'
        s += 'Lista de candidatos: ' + '\n'
        for t in self.candidatos:
            s += str(t) + '\n'
        s += '\n- - - - - - - - - - \n'
        return s

    def verificar_eligibilidade(self, eleitorId):
        '''
        Função que verifica se um eleitor identificado por eleitorId está na lista
        de eleitores válidos (self.eleitores). Para fins dessa simulação, ela sempre
        retorna True.
        '''
        return True

        

