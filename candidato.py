class Candidato:
    '''
    Classe que simula um candidato. Para esta simulação, apenas o nome e o número foram usados.
    Aqui entraria outras informações (foto, cargo, partido, legenda etc), que seriam armazenadas na urna.
    '''
    def __init__(self, nome, numero, id):
        self.nome = nome
        self.numero = numero
        self.id = id

    def __str__(self):
        s = '* * Candidato ' + str(self.id) + ' : '
        s += self.nome
        s += ' ' + str(self.numero)
        return s
