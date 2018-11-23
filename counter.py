from voto import Voto
from eleicao import Eleicao
from keys import PublicKey, PrivateKey
from ppk import ppk_verifica
from cipher import multiply
from elgamal import elgamal_decrypt
from elgamal_exp import elgamalexp_decrypt
from canalPublico import CanalPublico
import time

class Counter:
    '''
    Classe que simula um Counter. O Counter recebe uma instancia de Eleicao e gera dois vetores
    iniciados com valores nulos de tamanho do numero de candidatos da eleição. Esses dois vetores
    guardam os resultados parciais e os valores secretos criptografados. O counter também guarda
    o "canal público", representando a tabela para consulta dos votos após a eleição.
    '''
    def __init__(self, eleicao, privateKey):
        if not isinstance(eleicao, Eleicao):
            print('Tentativa de iniciar Counter com eleicao invalida')
            return None
        if not isinstance(privateKey, PrivateKey):
            print('Tentativa de iniciar Counter com chave privada invalida')
            return None

        self.eleicao = eleicao
        self.privateKey = privateKey
        self.resultado_parcial = [None for i in eleicao.candidatos]
        self.secreto_cifrado = [0 for i in eleicao.candidatos]
        self.canalPublico = []

    def atualiza_resultado_parcial(self, vetor):
        for i in range(0, len(vetor)):
            self.resultado_parcial[i] = multiply(self.resultado_parcial[i], vetor[i].votoCifrado, self.eleicao.publicKey)
            self.secreto_cifrado[i] += elgamal_decrypt(vetor[i].Scifrado, self.eleicao.publicKey, self.privateKey)
            if self.resultado_parcial[i] is None:
                print ('Erro atualizando resultado parcial.')
                return 
        print ('Resultados parciais atualizados')

    def computa_resultado(self):
        return [elgamalexp_decrypt(i, self.eleicao.publicKey, self.privateKey, self.eleicao.Neleitores*2 + 1) - self.eleicao.Neleitores for i in self.resultado_parcial]

    def print_canal_publico(self):
        for x in self.canalPublico:
            print(x)

        print('\nValores secretos: ')
        print(self.secreto_cifrado)

    def str_canal_publico(self):
        s = str(self.eleicao.publicKey) + '\n'
        s += 'Vetor secreto - ' + str(self.secreto_cifrado) + '\n\n'
        s += 'Primeira coluna: id do eleitor, segunda coluna: hash do voto, terceira coluna: bit commitment \n\n'
        for x in self.canalPublico:
            s += str(x.idEleitor) + ' - '
            s += str(x.hashVoto) + ' - '
            s += str(x.bitCom) + '\n'
        return s


    def recebe_voto(self, voto):
        '''
        Simulação do momento que o Counter recebe um voto e aceita (atualiza resultado, envia para 
        o canal publico, retorna True) 
        ou não (retorna False).
        As etapas de verificação são:
            1 - Verificar eligibilidade do eleitor;
            2 - Testar prova de conhecimento parcial total;
            3 - Testar prova de conhecimento parcial para cada votoElemento contido em Voto;

        Retornar False se qualquer um dos testes falhar. Se os testes passarem, atualiza o resultado
        parcial, envia informacoes para canal publico e retorna True.
        '''

        if not isinstance(voto, Voto):
            print('Counter recebeu voto invalido')
            return False

        if self.eleicao.verificar_eligibilidade(voto.idEleitor) is False:
            print('Eleitor ' + str(voto.idEleitor) + ' esta irregular. Voto rejeitado.')
            return False

        if ppk_verifica(voto.ppkY, self.eleicao.publicKey, len(self.eleicao.candidatos), len(self.eleicao.candidatos) + 1) is False:
            print('Teste da prova de conhecimento parcial total falhou. Voto Rejeitado')
            return False

        for i in range(0, len(voto.vetor)):
            if ppk_verifica(voto.vetor[i].ppk, self.eleicao.publicKey, 1, 2) is False:
                print('Teste da prova de conhecimento parcial falhou. Voto Rejeitado')
                return False

        self.atualiza_resultado_parcial(voto.vetor)

        self.canalPublico.append(CanalPublico(voto.idEleitor, voto.h, [b.bitCom for b in voto.vetor]))
        print('Counter recebeu e processou o voto com sucesso. \n')
