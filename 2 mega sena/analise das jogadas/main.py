from os import system, name
from time import sleep
from itertools import permutations

sequencias = []

def limpar():
  system('cls' if name == 'nt' else 'clear')

def transformarInteiro(seq):
  copysequencia = []
  for n in seq.split(' '):
    copysequencia.append(int(n))
  return copysequencia
def pegatotaldezena(seq):
  seq = transformarInteiro(seq)
  total = 0
  for n in seq:
    total += n
  return total
def pegatotalunidade(seq):
  soma = 0
  seq = seq.split(' ')
  for n in seq:
    for i in str(n):
      soma += int(i)
  return soma

def pega3iguais(numeros):
  copiaComCor = ''
  copiaSeparada = ''
  sequenciasEncontradas = []
  vezes = 0
  for sequencia in sequencias:
    for n in transformarInteiro(numeros):
      if n in transformarInteiro(sequencia):
        vezes += 1
    if vezes >= 3:
    
      copiaSeparada = numeros.split(' ')
      for numero in sequencia.split(' '):
        if '\n' in numero:
          numero = numero.replace('\n', '')
        if numero in copiaSeparada:
          copiaComCor += '\033[1;31m' + numero + '\033[0;0m' + ' '
        else:
          copiaComCor += numero + ' '

        copiaComCor = copiaComCor.replace('\n', '')

      sequenciasEncontradas.append(copiaComCor)
      copiaComCor = ''
      copiaSeparada = ''
    vezes = 0
  return 'nada encontrado' if len(sequenciasEncontradas) == 0 else sequenciasEncontradas
def somasUnidadesIguais(seq):
  sequenciasSalvas = []
  totaluni = int(seq)
  for sequencia in sequencias:
    sequencia = sequencia.replace('\n', '')
    if totaluni == pegatotalunidade(sequencia):
      sequenciasSalvas.append(sequencia)
  return 'nada encontrado' if len(sequenciasSalvas) == 0 else sequenciasSalvas
def somasDezenasIguais(seq):
  sequenciasSalvas = []
  totaldez = int(seq)
  for sequencia in sequencias:
    sequencia = sequencia.replace('\n', '')
    if totaldez == pegatotaldezena(sequencia):
      sequenciasSalvas.append(sequencia)
  return 'nada encontrado' if len(sequenciasSalvas) == 0 else sequenciasSalvas
def atualizarBanco():
  while True:
    limpar()
    resp = input("""
    1 - adicionar sequencia da mega-cena
    2 - adicionar sequencia da quina de são jõao

    """)

    limpar()
    sequencia = input("""digite a sequencia: 
    ex: 
    05 09 16 24 35 55
    
    """)

    if resp not in ['1', '2']:
      resp = 1

    if not len(sequencia.split(' ')) == 6 and resp == 1:
      print('sequencia não autorizada.')
      sleep(2)
      continue
    if not len(sequencia.split(' ')) == 5 and resp == 2:
      print('sequencia não autorizada.')
      sleep(2)
      continue

    arquivo2 = open(f'sequencias{resp}.txt', 'r')
    sequencias = arquivo2.read()
    arquivo2.close()
    arquivo = open(f'sequencias{resp}.txt', 'w')
    arquivo.write(f'{sequencia}\n{sequencias}')
    arquivo.close()

    limpar()
    print(sequencias)
    input('sequencia adicionada com sucesso!\npressione enter para continuar')
    return
def pegaProxNum(nun):

  def detecOcorrencias(lista, nun):
    ocorrencias = []
    indice = 0
    n = 0
    while True:
      if nun in lista:
        indice = lista.index(nun)
        if indice == len(lista) - 1:
          return ocorrencias
        ocorrencias.append(indice + n)
        lista.pop(indice)
        n += 1
      else:
        return ocorrencias  
  def quantOcorrencias(lista, ocorrencias):
    quant = dict()
    for ocorrencia in ocorrencias:
      ocorrencia += 1
      if lista[ocorrencia] in quant:
        quant[lista[ocorrencia]] = quant[lista[ocorrencia]] + 1
      else:
        quant[lista[ocorrencia]] = 1
    return quant
  def pegaTotal(ocorrencias):
    total = 0
    for quant in ocorrencias.values():
      total += quant
    return total
  def pegaPorcent(total, quant):
    return f'{(quant * 100) / total:.2f}'
  def naoApareceram(aparecidos, nun):
    texto = ''
    numeros = [*range(1, 60+1)]
    for chave in aparecidos:
      if chave in numeros:
        numeros.remove(chave)
    for n in numeros:
      texto += f'{n}, '
    return texto[0:-2]

  arquivo = open('sequencias1.txt', 'r')
  sequencia = transformarInteiro(arquivo.read().replace('\n', ' '))
  arquivo.close()
  ocorrencias = quantOcorrencias(sequencia, detecOcorrencias(sequencia.copy(), nun))
  total = pegaTotal(ocorrencias)
  azul = "\033[1;32m"
  normal = "\033[0;0m"

  if len(ocorrencias) == 0:
    print('nenhuma ocorrencia encontrada')
  else:
    c = 1
    for chave, valor in ocorrencias.items():
      print(f'{azul if c < 10 else normal}{c} - Nº {chave}, apareceu {valor} vezes com {pegaPorcent(total, valor)}%{normal}')
      c += 1
    print(f'\nos numeros que não apareceram foram:')
    print(naoApareceram(ocorrencias, nun))
def analisarSemelhrantes(seq):
  numeros = [*range(1, 60+1)]
  lista = []

  for num in permutations(seq.replace(' ', ''), 2):
    dezena = int(f'{num[0]}{num[1]}')

    if dezena <= 60 and dezena >= 1 and dezena not in lista:
      lista.append(dezena)
    
  for num in lista:
    if num in numeros:
      numeros.remove(num)

  if len(numeros) == 0:
    print('todos os numeros tiveram semelhança')
  else:
    print('Esses numeros não tem semelhança: ', end='')
    for n in numeros:
      print(n, end=' ')

def app():
  try:
    global sequencias
    resp = input("""
    1) utilizar a sequencia da mega-cena
    2) utilizar a sequencia da quina de são jõao
    """)
    if resp not in ['1', '2']:
      resp = 1

    arquivo = open(f'sequencias{resp}.txt', 'r')
    for sequencia in arquivo.readlines():
      sequencias.append(sequencia)
    arquivo.close()

    limpar()
    while True:
      while True: # pergunta as opções
        resp = input("""
    1) ver se a soma das unidades são iguais
    2) ver se a soma das dezenas são iguais
    3) colocar 3 ou mais numeros e ver se tem pelo menos tres neles em alguma sequencia
    4) atualizar banco de dados
    5) analisar proximos numeros
    6) analisar semelhantes
    coloque apenas um numero ex:
    1
    3

    """)
        if resp not in ['1', '2', '3', '4', '5', '6']:
          limpar()
          print("digite uma opção valida")
        else:
          break
      limpar()
      while True: # configura a variavel sequencia para a opção 1 e 2
        if resp in ['1', '2', '5']:
          numeros = input("""digite o numero que deseja verificar:
    ex:
    95
    154

    """)
          if not numeros.isdigit():
            limpar()
            print("digite numeros validos")
          else:
            break
        else:
          break
      limpar()
      while True: # configura a sequencia numeros para a opção 3
        if resp in ['3', '6']:
          numeros = input("""digete os numeros que deseja procurar:
    ex:
    '04 06 09'
    '06 16 18 31 50 56'

    """)
          if not len(numeros.split(' ')) <= 6 and not len(numeros.split(' ')) >= 3:
            limpar()
            print("digite de 3 a 6 numeros")
          else:
            break
        else:
          break
      limpar()

      if resp == '1':
        print('iniciando a busca por unidades iguais')
        resposta = somasUnidadesIguais(numeros)
        if resposta == 'nada encontrado':
          print(resposta)
        else:
          for sequencia in resposta:
            print(sequencia)
          input('\npressione enter para continuar')

      elif resp == '2':
        print('iniciando a busca por dezenas iguais')
        resposta = somasDezenasIguais(numeros)
        if resposta == 'nada encontrado':
          print(resposta)
        else:
          for sequencia in somasDezenasIguais(numeros):
            print(sequencia)
        input('\npressione enter para continuar')

      elif resp == '3':
        print('iniciando a busca por 3 iguais')
        resposta = pega3iguais(numeros)
        if resposta == 'nada encontrado':
          print(resposta)
        else:
          for sequencia in pega3iguais(numeros):
            print(sequencia)
        input('\npressione enter para continuar')

      elif resp == '4':
        atualizarBanco()

      elif resp == '5':
        pegaProxNum(int(numeros))
        input('\npressione enter para continuar')

      elif resp == '6':
        print('iniciando a busca por semelhantes')
        analisarSemelhrantes(numeros)
        input('\npressione enter para continuar')

      else:
        print('opção invalida')
        input('pressione enter para continuar')
      limpar()
  except Exception as error:
    limpar()
    print(f'erro... {error}\n')
    app()
app()