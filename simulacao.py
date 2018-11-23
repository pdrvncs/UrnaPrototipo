from eleicao import Eleicao
from counter import Counter
from urna import Urna
from candidato import Candidato
from eleitor import Eleitor
from voto import Voto
import random
from keys import gera_par_de_chaves
import time
from os import path

def sim_cria_candidato_aleatorio(id):
    primeiro_nome = ['Alipio', 'Alice', 'Bob', 'Carole', 'Eve', 'Toshio', 'Omar', 'Varg', 'Glen' ]
    segundo_nome = ['Cranicola', 'Almeida', 'Silva', 'Messias', 'Oliveira', 'Pereira', 'Hellhammer', 'Virkernes', 'Costa', 'Eneas', 'Serra', 'Nascimento']
    nome_do_candidato = random.choice(primeiro_nome) + ' ' + random.choice(segundo_nome)
    numero_do_candidato = int(str(random.randint(1,9)) + str(random.randint(1,9)) + str(random.randint(1,9)) + str(random.randint(1,9)))

    return Candidato(nome_do_candidato, numero_do_candidato, id)

candidatos = []
eleitores = []
eleicao = None
publicKey = None
privateKey = None
counter = None
urna = None


opt = 0
while opt < 1 or opt > 2:
    print('1) Iniciar nova eleicao')
    print('2) Auditar canal publico')
    opt = int(input())

if opt == 1:

    print ('Informe a quantidade de candidatos da eleicao')
    n = int(input())

    for i in range(0, n):
        candidatos.append(sim_cria_candidato_aleatorio(i))

    print ('Informe a quantidade de eleitores')
    m = int(input())

    for i in range(0, m):
        eleitores.append(Eleitor(random.randint(1000, 99999)))

    bits = 0
    while bits <= 0:
        print ('Informe o tamanho da chave em bits')
        bits = int(input())

    keys = gera_par_de_chaves(bits)
    publicKey = keys['publicKey']
    privateKey = keys['privateKey']

    eleicao = Eleicao(publicKey, privateKey, eleitores, candidatos)
    urna = Urna(publicKey, candidatos)
    counter = Counter(eleicao, privateKey)

    print(eleicao)
    f_eleicao = open('eleicao.txt', 'w+')
    f_eleicao.write(str(eleicao))
    print('Informacoes da eleicao geradas no arquivo eleicao.txt')
    f_eleicao.close()
    for i in range(0, len(eleitores)):
        print('Insira o numero do candidato do eleitor ' + str(i))
        escolha = None
        while escolha is None:
            escolha = eleicao.encontra_candidato(int(input()))
        v = urna.vota(i, escolha.numero)
        nome_arquivo_cedula = 'cedula ' + str(i) + '.txt'
        f_voto = open(nome_arquivo_cedula, 'w+')
        f_voto.write(str(v))
        print('Cedula gerada no arquivo ' + nome_arquivo_cedula)
        f_voto.close()
        counter.recebe_voto(v)            

    print('Eleicao finalizada.')

    print('\n\n * * * * * * \nComputando resultados...')
    resultado = counter.computa_resultado()
    for x, y in zip(eleicao.candidatos, resultado):
        print(x.nome + ' : ' + str(y) + ' votos')

    f_canal = open('canal publico.txt', 'w+')
    f_canal.write(counter.str_canal_publico())
    f_canal.close()
    print('Canal publico gerado no arquivo canal publico.txt')

else:   
    if path.isfile('./canal publico.txt'):
        with open('canal publico.txt') as f:
            lines = f.readlines()
            aux = lines[5].split(' - ')[-1]
            nCandidatos = len(aux.split(','))  # descobre numero de candidatos da eleicao
            
            pkSplit = lines[0].split(' -> ')  # le chave publica
            pk = [int(''.join(c for c in x if c not in '([,\n])')) for x in pkSplit[-1].split(', ')]
            p, g, beta = pk[0], pk[1], pk[2]  
            
            pkSplit = lines[1].split(' - ')  # le vetor secreto
            vetorSecreto = [int(''.join(c for c in x if c not in '([,\n])')) for x in pkSplit[-1].split(', ')]

            nEleitores = 0

            opt = -1
            while opt < 0 or opt > nCandidatos - 1:
                print('Informe o indice do candidato a ser auditado (0 - ' + str(nCandidatos - 1) + ')')
                opt = int(input())
            bitcoms = []
            for l in lines:
                split = l.split(' - ')
                if l[0].isdigit() is False:
                    continue
                bitc = [int(''.join(c for c in x if c not in '[,\n]')) for x in split[-1].split()]
                bitcoms.append(bitc)
                nEleitores += 1
            
            print('Multiplicando coluna do candidato ' + str(opt) + '...')
            mul = 1
            for b in bitcoms:
                mul = mul * b[opt]
            mul %= p
            print('Valor obtido : ' + str(mul))
            result = -1
            while result < 0:
                print('Informe o resultado divulgado para o candidato ' + str(opt) + ': ')
                result = int(input())
                mul2 = (pow(g, vetorSecreto[opt], p) * pow(beta, result + nEleitores, p)) % p
                if mul == mul2:
                    print('Teste de auditacao passou')
                else:
                    print('Teste de auditacao nao passou. Resultado obtido: ' + str(mul2) + ' Resultado esperado: ' + str(mul))
        f.close()
    else:
        print('Arquivo canal publico.txt nao encontrado')
    