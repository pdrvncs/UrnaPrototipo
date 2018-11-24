# UrnaPrototipo

Executar o arquivo simulacao.py. A simulação permite duas opções: criar uma eleição do zero e auditar uma eleição finalizada.

1) Criando uma nova eleição.
  - Entre com a quantidade de candidatos, de eleitores e o tamanho em bits da chave.
  - A simulação vai gerar uma lista de candidatos fictícios com números aleatórios. As informações da eleição e das chaves utilizadas serão geradas no arquivo "eleicao.txt".
  - Para cada eleitor, entre com o número do candidato escolhido.
  - A "cédula" de cada eleitor x vai ser gerada em um arquivo "cedulax.txt".
  - Ao final do processo, a tabela para auditação será gerada no arquivo "canal publico.txt" e os resultados para cada candidato serão apresentados. 
  
2) Auditando uma eleição
  - A simulação irá abrir o arquivo "canal publico.txt".
  - Entre com a identificação do candidato a ser auditado, como listado no arquivo "eleicao.txt".
  - Entre com o resultado publicado para o candidato ao final do processo de eleição.
  - A simulação irá testar se os valores no arquivo "canal publico.txt" condizem com o resultado divulgado para o candidato.
