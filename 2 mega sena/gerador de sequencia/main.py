from random import choice, randint
from time import asctime
from os import system, name

# variaveis
numeros = [*range(1, 60+1)]
simetricos = [[1,10,51,60],
[2,9,59,52],
[3,8,58,53],
[4,7,57,54],
[5,6,55,56],
[6,5,55,6],
[7,4,57,54],
[8,3,53,58],
[9,2,52,59],
[10,1,51,60],
[11,20,41,50],
[12,42,19,49],
[13,18,43,48],
[14,17,44,47],
[15,16,45,46],
[16,46,45,15],
[17,14,44,47],
[18,13,43,48],
[19,12,42,49],
[20,11,50,41],
[21,30,31,40],
[22,32,29,39],
[23,28,38,33],
[24,27,37,34],
[25,26,35,36],
[26,25,35,36],
[27,24,34,37],
[28,23,33,38],
[29,39,22,32],
[30,21,31,40],
[31,21,30,40],
[32,22,39,29]]
sequenciasGeradas = []
minimo = 150
maximo = 250
quadrante = {
  1: [1,2,3,4,5,11,12,13,14,15,21,22,23,24,25],
  2: [6,7,8,9,10,16,17,18,19,20,26,27,28,29,30],
  3: [31,32,33,34,35,41,42,43,44,45,51,52,53,54,55],
  4: [36,37,38,39,40,46,47,48,49,50,56,57,58,59,60]
  }
intervalosSimetricos = [
[45, 30, 15,],
[59, 44, 29, 14],
[58, 43, 28, 13],
[57, 42, 27, 12],
[56, 41, 26, 11],
[55, 40, 25, 10],
[54, 39, 24, 9],
[53, 38, 23, 8],
[52, 37, 22, 7],
[51, 36, 21, 6],
[50, 35, 20, 5],
[49, 34, 19, 4],
[48, 33, 18, 3],
[47, 32, 17, 2],
[46, 31, 16, 1]
]
# transformando sequencias em inteiros : transformando sequencias em inteiros
def transformarInteiro(seq):
  copysequencia = []
  for n in seq:
    copysequencia.append(int(n))
  return copysequencia

arquivo = open('sequencias.txt', 'r')
seq1 = transformarInteiro(arquivo.readline().split(' '))
seq2 = transformarInteiro(arquivo.readline().split(' '))
seq3 = transformarInteiro(arquivo.readline().split(' '))
arquivo.close()
sequencias = [seq1, seq2, seq3]

# funções de funcionalidade
def pegatotal(seq):
      total = 0
      for n in seq:
        total += n
      return total
def pegaseq(seq):
      intervalo = []
      max = len(seq)
      for n in range(len(seq)-1):
        if n == max:
          break
        else:
          intervalo.append(seq[n] - seq[n+1])
      return intervalo
def retirasimetricos():
  for lista in simetricos:
    for n in lista:
      if n in seq1:
        for n in lista:
          if n in numeros:
            numeros.remove(n)
        break
def analisaseqrev(seq): # testar
  for n in range(-1, -7, -1):
    if seq[n] != numeros[-1]:
      return aumentaseq(seq, n)
def aumentaseq(seq, n): # testar
  seq[n] = numeros[numeros.index(seq[n])+1]
  for n in range(n+1, 0):
    seq[n] = numeros[0]
  return seq

# filtros
def filtro1(): # retira os numeros das 3 ultimas sequencias da mega sena
  for seq in sequencias:
    for n in seq:
      if n in numeros:
        numeros.remove(n)
def filtro2(sequencia): # retira a sequencia se tiver mais que dois intervalos igual, se tiver mais que 4 impares ou pares ou numeros repetidos
  intervalo = pegaseq(sequencia)
  p = 0
  i = 0
  for n in intervalo:
    if intervalo.count(n) > 2 or n == 0:
      # print('filtro2')
      return False
  for num in sequencia:
    if num % 2 == 0:
      p += 1
    else:
      i += 1
  if p > 4 or i > 4:
    # print('filtro2')
    return False
  for num in sequencia:
    if sequencia.count(num) > 1:
      # print('filtro2')
      return False
  return True
def filtro3(sequencia, min=150, max=250): # se caso a soma dos numeros for maior que 250 e menor que 150 sera retirada
  total1 = pegatotal(sequencia)
  if total1 > min and total1 < max:
    return True
  # print('filtro3')
  return False
def filtro4(sequencia): # se a soma dos numeros da ultima sequencia da mega sena for igual a soma da sequencia gerada, ela sera excluida
  total1 = pegatotal(sequencia)
  total2 = pegatotal(sequencias[0])
  if total1 == total2:
    # print('filtro4')
    return False
  return True
def filtro5(sequencia): # se caso o intervalo da ultima sequencia da mega sena for igual e no mesmo lugar que da sequencia gerada, ela sera excluida
  intervalo = pegaseq(sequencia)
  ultimointervalo = pegaseq(sequencias[0])

  for n in range(len(intervalo)):
    if intervalo[n] == ultimointervalo[n]:
      # print('filtro5')
      return False
    return True
def filtro6(): # retira sequencias que sejam simetricas
  retirasimetricos()
def filtro7(sequencia): # pega todas as sequencias anteriores dá mega sena, se caso tiver mais que 3 numeros iguais, no mesmo lugar, é retirada
  arquivo = open('sequencias.txt', 'r')
  for linha in arquivo.readlines():
    i = 0
    if linha == '\n':
      pass
    linha = transformarInteiro(linha.split(' '))
    for n in range(6):
      if sequencia[n] == linha[n]:
        i += 1
    if i > 3:
      # print('filtro7')
      arquivo.close()
      return False
  arquivo.close()
  return True
def filtro8(sequencia): # verifica se tem pelo menos um numero da sequencia em cada quadrante
  esta = False
  for numeroquadrante in quadrante:
    for numero in sequencia:
      if numero in quadrante[numeroquadrante]:
        esta = True
    if esta == False:
      # print('filtro8')
      return False
    esta = False
  return True
def filtro9(sequencia): # se a simetria dos intervalos bater com a da ultima jogada, e bater com a simetria da lista, ela sera excluida
  ultimoJogo = pegaseq(sequencias[0])
  intervalo = pegaseq(sequencia)
  simetricos = []
  for n in ultimoJogo:
    for intervalos in intervalosSimetricos:
      if n*-1 in intervalos:
        simetricos.append(intervalos)

  for n in intervalo:
    for intervalos in simetricos:
      if n*-1 in intervalos:
        return False
  
  return True
 
# junta todos os filtros
def filtros(seq):
  global r2
  resp = []
  filtro = True

  if r2 != 'todos':
    resposta = r2.split(' ')
    for n in resposta:
      resp.append(int(n))
  else:
    resp = range(1, 11)
  
  if 2 in resp:
    if not filtro2(seq):
      filtro = False
  if 3 in resp:
    if not filtro3(seq, minimo, maximo):
      filtro = False
  if 4 in resp:
    if not filtro4(seq):
      filtro = False
  if 5 in resp:
    if not filtro5(seq):
      filtro = False
  if 7 in resp:
    if not filtro7(seq):
      filtro = False
  if 8 in resp:
    if not filtro8(seq):
      filtro = False
  if 9 in resp:
    if not filtro9(seq):
      filtro = False
  if filtro:
    if not seq in sequenciasGeradas:
      sequenciasGeradas.append(seq)
      return True
    
# gera sequencias proximas
def proximos(seq, prox, q):

  t = asctime()
  t = t.split(' ')[3]
  t = t.split(':')[1]
  t = int(t)

  print('gerando sequencias proximas a sequencia: ', seq, 'com uma proximidade de: ', prox)
  for y in range(q):
    while True:

      t2 = asctime()
      t2 = t2.split(' ')[3]
      t2 = t2.split(':')[1]
      t2 = int(t2)

      sequencia = []
      for n in seq:
        sequencia.append(randint(n-prox if n >= 1+prox else 1, n+prox if n <= 60-prox else 60))
      if sequencia == seq:
        continue
      if filtros(sequencia):
        break

      if t2 == t+1:
        print('tempo esgotado')
        break

# gera uma sequencia a partir da variavel numeros
def gerasequencias(numeros, r):

  while True:
    try:
      t = asctime()
      t = t.split(' ')[3]
      t = t.split(':')[1]
      t = int(t)
    except:
      pass
    break

  for n in range(r):
    while True:
      
      while True:
        try:
          t2 = asctime()
          t2 = t2.split(' ')[3]
          t2 = t2.split(':')[1]
          t2 = int(t2)
        except:
          pass
        break

      seq = []
      for m in range(6):
        seq.append(choice(numeros))
      seq.sort()
      if filtros(seq):
        break

      if int(t2) == int(t)+1:
        print('tempo esgotado')
        break

# funcao principal
def app():
  global r1, r2, sequenciasGeradas, minimo, maximo
  while True:
    sequencia = []
    sequenciasGeradas = []
    minimo = 150
    maximo = 250

    # try: 
    system('cls' if name == 'nt' else 'clear') # escolhe o tipo de geração
    r1 = input("""
    1 - gerar sequencias aleatórias
    2 - gerar sequencias proximas a uma sequencia
    pode escolher apenas 1
    ex: 1
    ex: 2

    """)
    if (r1 in ['', ' ']):
      r1 = 1
    elif (not r1.isdigit()) or (len(r1) > 1):
      print('opçao invalida na primeira pergunta\n')
      input('pressione enter para continuar')
      continue
    else:
      r1 = int(r1)
    if (r1 > 2 and r1 < 1):
      print('opçao invalida na primeira pergunta\n')
      input('pressione enter para continuar')
      continue
    system('cls' if name == 'nt' else 'clear') # escolhe os filtros
    r2 = input("""
    escolha os filtros:
    1 - retira os numeros das 3 ultimas sequencias da mega sena
    2 - retira a sequencia se tiver mais que dois intervalos igual, se tiver mais que 4 impares ou pares ou numeros repetidos
    3 - se caso a soma dos numeros for maior que 250 e menor que 150 sera retirada
    4 - se a soma dos numeros da ultima sequencia da mega sena for igual a soma da sequencia gerada, ela sera excluida
    5 - se caso o intervalo da ultima sequencia da mega sena for igual e no mesmo lugar que da sequencia gerada, ela sera excluida
    6 - retira sequencias que sejam simetricas
    7 - pega todas as sequencias anteriores dá mega sena, se caso tiver mais que 3 numeros iguais, no mesmo lugar, é retirada
    8 - retira a sequencia que não tiver pelo menos um numero em cada quadrante
    9 - retira as sequencias que tiver os numeros na lista de intervalos simétricos a partir do intervalo da ultima sequencia da mega sena
    pode escolher varios filtros
    ex: 1 2 5 7
    ex: 1 3 7
    ex: todos

    """)
    if (r2 in ['', ' ']):
      r2 = 'todos'
    system('cls' if name == 'nt' else 'clear') # a quantidade de sequencias
    r3 = input("""
    escolha a quantidade de sequencias que deseja gerar:
    ex: 10

    """)
    system('cls' if name == 'nt' else 'clear') # ver se tem algum erro nas opções
    if (r3 in ['', ' ']):
      r3 = 10
    elif (not r3.isdigit()) or (len(r3) < 1):
      print('opçao invalida na terceira pergunta\n')
      input('pressione enter para continuar')
      continue
    else:
      r3 = int(r3)
    
    resp = [] # arruma as opções de filtros
    if r2 != 'todos':
      resposta = r2.split(' ')
      for n in resposta:
        resp.append(int(n))
    else:
      resp = range(1, 11)
    
    if 1 in resp: # coloca o filtro 1 e 6 pra funcionar
      filtro1()
    if 6 in resp:
      filtro6()

    if 3 in resp:
      diferenca = input("""
    média da sequencia 3, deixe vazio caso não queira mudar
    ex: 100 350

      """)
      if diferenca in ['', ' ']:
        pass
      else:
        minimo, maximo = diferenca.split(' ')
        minimo = int(minimo)
        maximo = int(maximo)

    # gera sequencias aleatórias, sequencias 1
    system('cls' if name == 'nt' else 'clear')
    if r1 == 1:
      print('\ngerando as sequencias\npor favor aguarde...')

      gerasequencias(numeros, r3)
      if sequenciasGeradas == []:
        print('nenhuma sequencia gerada')
      else:
        print('\nsequencias geradas:\n')

        for n in sequenciasGeradas:
          x = ''
          for i in n:
            x += f'{i} '
          sequencia.append(x)
        for seq in sequencia:
          print(seq) 

      while True:
        r = input('quer que seja salvo em um arquivo? (s/n)')
        if r == 's':

          system('cls' if name == 'nt' else 'clear')
          arquivo = open('sequencias salvas.txt', 'w')
          arquivo.write('sequencias geradas:\n')
          for seq in sequencia:
            arquivo.write(f'{seq}\n')
          arquivo.close()
          print('salvo com sucesso no arquivo \'sequencias salvas.txt\'')

          input('pressione enter para continuar')
          break
        input('pressione enter para continuar')
        break
    
    # gera sequencias proximas, gera sequencias 2
    system('cls' if name == 'nt' else 'clear')
    if r1 == 2:
      while True:
        r4 = input("""
    quão proximo você quer que as sequencias sejam?
    ex: 1
    ex: 5

    """)
        system('cls' if name == 'nt' else 'clear')
        r5 = input("""
    qual será a sequencia a ser analisada?
    ex: 1 7 25 32 45 60

    """)

        if (r4 in ['', ' ']) or (not r4.isdigit()) or (int(r4) < 1):
          print('opçao invalida na quarta pergunta\n')
          input('pressione enter para continuar')
          continue
        else:
          r4 = int(r4)
        
        if (r5 in ['', ' ']):
          print('opçao invalida na quinta pergunta\n')
          input('pressione enter para continuar')
          continue
        else:
          r5 = transformarInteiro(r5.split(' '))
        break

      system('cls' if name == 'nt' else 'clear')
      print('\ngerando as sequencias\npor favor aguarde...')
      proximos(r5, r4, r3)
      if sequenciasGeradas == []:
        print('nenhuma sequencia gerada')
      else:
        print('\nsequencias geradas:\n')

        for n in sequenciasGeradas:
          x = ''
          for i in n:
            x += f'{i} '
          sequencia.append(x)
        for seq in sequencia:
          print(seq) 

      while True:
        r = input('quer que seja salvo em um arquivo? (s/n)')
        if r == 's':
          system('cls' if name == 'nt' else 'clear')
          arquivo = open('sequencias salvas.txt', 'w')
          arquivo.write('sequencias geradas:\n')
          for seq in sequencia:
            arquivo.write(f'{seq}\n')
          arquivo.close()
          print('salvo com sucesso no arquivo \'sequencias salvas.txt\'')

          input('pressione enter para continuar')
          break
        input('pressione enter para continuar')
        break

    # except Exception as erro:
    #   system('cls' if name == 'nt' else 'clear')
    #   print(f'erro encontrado:\n{erro}\ncontate o desenvolvedor')
    #   input('pressione enter para continuar')

app()