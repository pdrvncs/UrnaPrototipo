class VotoElemento:
    def __init__(self, votoCifrado, Scifrado, bitCom, ppk):
        '''
        votoCifrado : o voto do eleitor para o candidato associado, encriptado com ElGamal Exponencial
        Scifrado    : o numero secreto S utilizado, encriptado com ElGamal
        bitCom      : a cifra Bit Commitment para esse elemento
        ppk         : prova de conhecimento parcial para esse elemento
        '''
        self.votoCifrado = votoCifrado
        self.Scifrado = Scifrado
        self.bitCom = bitCom
        self.ppk = ppk

class Voto:
    '''
    Classe representando o voto que é gerado pela urna e enviado para o Counter
    '''
    def __init__(self, idEleitor, vetor, ppkY, h):
        '''
        idEleitor : a identificação do eleitor
        vetor     : um vetor de tamanho N do tipo VotoElemento
        ppkY      : prova de conhecimento parcial para vetor (o total)
        h         : hash desse voto
        '''
        self.idEleitor = idEleitor
        self.vetor = vetor
        self.ppkY = ppkY
        self.h = h

    def __str__(self):
        s = ' - - Voto - -\n'
        s += 'Eleitor : ' + str(self.idEleitor) + '\n'
        s += 'Hash    : ' + str(self.h) + '\n'
        s += 'Prova Y : \n' + str(self.ppkY) + '\n'
        i = 0
        s += '\n - - - Vetor de candidatos - - -\n'
        for v in self.vetor:
            s += '\n * Candidato ' + str(i) + '\n'
            s += ' * * Cifra          :  ' + str(v.votoCifrado) + '\n'
            s += ' * * S cifrado      :  ' + str(v.Scifrado) + '\n'
            s += ' * * Bit Commitment :  ' + str(v.bitCom) + '\n'
            s += ' * * PPK            : \n' + str(v.ppk) + '\n'
            i += 1
        s += '- - Fim Voto - -\n'

        return s

