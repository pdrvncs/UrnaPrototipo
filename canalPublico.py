class CanalPublico:
   def __init__(self, idEleitor, hashVoto, bitCom):
       self.idEleitor = idEleitor
       self.hashVoto = hashVoto
       self.bitCom = bitCom

   def __str__(self):
        s = '\n'
        s += 'Identificao do eleitor   : ' + str(self.idEleitor) + '\n'
        s += 'Hash                     : ' + str(self.hashVoto) + '\n'
        s += 'Bit Commitment associado : ' + str(self.bitCom)

        return s