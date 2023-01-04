from time import sleep, localtime
from requests import get
from datetime import datetime

jogos = []
estrategias = []
logs = {}
token = '5193397913:AAEmsAdE2IRVTNDLe5qLaMsG3y_S61t-zrA'
link = f"https://api.telegram.org/bot{token}/"
stop2 = False
versao = 6
idParcial = None
parcial_hora = {'green': 0, 'green branca': 0, 'red': 0}
hora = localtime().tm_hour
horaAHora = {}
atualizado = False
dia = False

stickers = {'green branco': 'CAACAgEAAxkBAAEV-aRi0CM01C2fXvxjej6OZ8f0NAzvbgACjgEAAmZluEUPF-6vdM99sCkE',
'green': 'CAACAgEAAxkBAAEV-Ypi0CCV0uBoGuwowPX0T8LHbGWwxwAC8gEAAqTwIUViqOsX-tT1cikE',
'loss': 'CAACAgEAAxkBAAEV-ZRi0CEHy0s0uYaIsv6RzqJ_4RlpewACGAIAAp0pKUW3qhl-6XSkwikE',
'greens seguidos': 'CAACAgEAAxkBAAEV-Z5i0CGkyOOL3cIalsuMVxmxYAVDXgAC_AEAAqLCIEWL8D1Oy-u_UikE'}

#        grupo principal
grupo = ['-861832842']
#             privado
grupo_pv = []

chat = grupo[0]

try:

  def manda_msg(msg, chats=grupo):
    global token
    resp = []
    for chat in chats:
      resp.append(get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat}&text={msg}").json())
    return resp

  def verifica_hora():
    global dia
    global hora
    global parcial_hora
    global horaAHora
    global atualizado

    if atualizado == True and datetime.today().weekday() == 2:
      atualizado = False

    if datetime.today().weekday() == 1 and atualizado == False:

      manda_msg(f'atualização nos padrões da blaze detectado.\naguarde até o bot detectar os novos padrões.\nperiodo aproximado até o bot detectar os novos padrões: 24hrs.')
      logs = {}
      for estrategia in estrategias:
        logs[str(estrategia['sequencia'])] = {1: {'green': 0, 'green branca': 0, 'red': 0, 'acertividade': 0}, 2: {'green': 0, 'green branca': 0, 'red': 0, 'acertividade': 0}}

      horaAHora = {}
      parcial_hora = {'green': 0, 'green branca': 0, 'red': 0}
      atualizado = True

    elif localtime().tm_hour != hora:
      hora = localtime().tm_hour

      if hora == 1 and dia == True:
        dia = False

      if hora == 0 and dia == False:
        parcial = ((parcial_hora["green"] + parcial_hora['green branca']) * 100) / (parcial_hora["green"] + parcial_hora['green branca'] + parcial_hora['red'])
        horaAHora[hora] = parcial
        listinha = []

        for valor in horaAHora.values():
          listinha.append(valor)

        manda_msg(f'Relatório do dia:\nA média do dia foi de: {sum(listinha) / len(listinha):.2f}% 🎯')
          
        txt = ''
        for n, x in enumerate(sorted(horaAHora, key=horaAHora.get, reverse=True)):
          if n == 11:
            break
          txt += f'{n+1} - hora: {x} acertividade {horaAHora[x]:.2f}\n'

        manda_msg(f'As top 10 melhores horas de hoje: 🍀🍀🍀\n{txt}')

        horaAHora = {}
        dia = True

      elif parcial_hora['green'] != 0 or parcial_hora['green branca'] != 0 or parcial_hora['red'] != 0:
        manda_msg(f'relatório da ultima hora:\n✅ = {parcial_hora["green"]}\n⚪️ = {parcial_hora["green branca"]}\n⛔️ = {parcial_hora["red"]}\n🎯 = {parcial:.2f}')
          
      elif parcial_hora['green'] != 0 or parcial_hora['green branca'] != 0 or parcial_hora['red'] != 0:
        parcial = ((parcial_hora["green"] + parcial_hora['green branca']) * 100) / (parcial_hora["green"] + parcial_hora['green branca'] + parcial_hora['red'])
        horaAHora[hora] = parcial
        manda_msg(f'relatório da ultima hora:\n✅ = {parcial_hora["green"]}\n⚪️ = {parcial_hora["green branca"]}\n⛔️ = {parcial_hora["red"]}\n🎯 = {parcial:.2f}')
      
      parcial_hora = {'green': 0, 'green branca': 0, 'red': 0}

  def manda_sticker(sticker, chats=grupo):
    global token
    for chat in chats:
      get(f'https://api.telegram.org/bot{token}/sendSticker?chat_id={chat}&sticker={sticker}')

  def ns(estrategia):
    global estrategias
    estrategias.append({'sequencia': estrategia, 'aposta': ['p', 'b'], 'tipo': 1})
    estrategias.append({'sequencia': estrategia, 'aposta': ['v', 'b'], 'tipo': 2})

  for i1 in range(1, 15):
    for i2 in range(1, 15):
      ns([i1, i2])

  for estrategia in estrategias:
    logs[str(estrategia['sequencia'])] = {1: {'green': 0, 'green branca': 0, 'red': 0, 'acertividade': 0}, 2: {'green': 0, 'green branca': 0, 'red': 0, 'acertividade': 0}}

  def mensagem(msg):
    while True:
      try:
        return get(f"{link}sendMessage?chat_id={chat}&text={msg}").json()
      except:
        pass

  def quantidades_jogadas(chave, n):
    return int(logs[str(chave)][n]['green'] + logs[str(chave)][n]['green branca'] + logs[str(chave)][n]['red'])

  def ouve():

    mensagens = []

    while True:
      try:
        r = get(f'{link}getUpdates').json()
        resultados = r['result']
        break
      except:
        pass

    for resultado in resultados:
      try:
        mensagens.append({'update_id': resultado['update_id'], 'from_id': resultado['message']['from']['id'], 'chat_id': resultado['message']['chat']['id'], 'text': resultado['message']['text']})
      except:
        pass

    ids = []
    for mensagem in mensagens:
      r = comandos(mensagem['text'], mensagem)
      if r:
        ids.append(mensagem["update_id"])

    for idm in ids:
      while True:
        try:
          r = get(f'{link}getUpdates?offset={int(idm)+1}').json()
          break
        except:
          pass

  def comandos(text, conteudo):
    global chat
    global permicao
    global logs
    global stop2
    global versao

    if conteudo['chat_id'] == int(chat):

      if conteudo['from_id'] == 5027889205:

        if text == '/reset-parcial':
          logs = {}

          for estrategia in estrategias:
            logs[str(estrategia['sequencia'])] = {1: {'green': 0, 'green branca': 0, 'red': 0, 'acertividade': 0}, 2: {'green': 0, 'green branca': 0, 'red': 0, 'acertividade': 0}}

          mensagem('parcial resetado\nespere até o bot identificar os novos padrões!!')

        if text == '/help-adm':
          mensagem('comandos restritos:\n\n/reset-parcial - para resetar o parcial do bot\n/atualizar - para atualizar o bot manualmente\n/topadm - mandar um relatório completo pros adm')

        if text == '/atualizar':
          mensagem('atualizando')
          stop2 = True

        if text == '/topadm':
          texto = f'as melhores das {len(logs)*2} estratégias\n'
          lista = []
          n = 1

          for log in logs.items():
            lista.append([log[1][1]['acertividade'] - log[1][1]['red'], n, log[1][1]['green'], log[1][1]['green branca'], log[1][1]['red']])
            n+=1
            lista.append([log[1][2]['acertividade'] - log[1][2]['red'], n, log[1][2]['green'], log[1][2]['green branca'], log[1][2]['red']])
            n+=1

          if not lista:
            mensagem('poucos dados para fazer o top...\ntente novamente mais tarde')
            return True

          top = list(sorted(lista, key=lambda dados: int(dados[0]), reverse=True))

          for i in top:
            texto += f'{i[0]}% - nº:{i[1]}, g:{i[2]}, b:{i[3]}, r:{i[4]}\n'

          while True:
            try:
              get(f"{link}sendMessage?chat_id=5027889205&text={texto}")
              break
            except:
              pass

      elif text in ['/reset-parcial', '/help-adm', '/atualizar', '/topadm']:
        mensagem('você não tem permissão suficiente')

      if text == '/version':
        mensagem(f'a versão atual é: {versao}')

      if text == '/parcial':
        parcial = retorna_parcial()
        mensagem(parcial)

      if text == '/teste':
        mensagem('funcionando!')

      if text == '/help':
        mensagem('''os comandos atuais são:
  /version - para ver a versão atual do bot
  /teste - para ver se o bot ta funcionando
  /help - para ver os comandos
  /parcial - para mostrar o parcial atual do bot
  /help-adm - para ver os comandos de adm
  /mudancas - para var o que veio junto a atualização do bot
  /pravir - mostrar o que estamos pensando pro futuro
  /sugestao - para você mandar uma sugestão diretamente para os desenvolvedores
  /ajudaADM - para mandar ajuda diretamente pros ADM
  ''')

      if text == '/mudancas':
        mensagem('''o que veio na atialização 5:
  - sistema de +80%:
  As estratégias estãram desabilitadas se caso a acertividade das mesmas estiverem menor que 80%.
  - catalogação das estrategias:
  Agora é o Bot que ira formar, filtrar, recomendar e mostrar as estratégias que ele achar melhor, juntamente com a atualização de +80%, decidimos o bot formar e filtrar as melhores estratégias, sendo formadas e administradas pelo bot +ou- 400 estratégias.
  - sistema de aviso automatico de erro:
  Uma coisa que estava faltando era um aviso de erro, as vezes, nas partes de teste, podemos deixar passar coisas que vão ser vistas tarde demais, e se caso já tiver sido atualizada para o grupo vip, o bot ira mandar uma mensagem automatica para o programador avisando sobre o erro.
  É claro que é sempre bom a comunidade avisar tambem, podendo dar sempre um /ajudaADM para nos avisar sobre algum eventual problema ou bug
  - remoção do comando /top
  Comando onde mostrava as melhores estratégias, porem por conta do grande numero de estratégias, foi modificado para mostrar a acertividade da estratégia em relação a acertividade global.
  - relatório de hora e dia
  Agora com um relatório detalhado de hora em hora de como ta o dia, e de dia em dia das melhores horas.
  - fix de alguns bugs.
        ''')

      if text == '/pravir':
        mensagem('''
  - Estratégias pro branco.
  - Sistema de SPAN.
  - Salas de Sinais para outros sites.
  - Salas de Sianis para diferentes gales.
  - Bot Aposta Automatica.
  - Pacotes Adicionais Para Venda:
  - promoções ou pagamentos:
  - PDFs e videos para iniciantes:
  - Canal da Comunidade:
  - Site do Magic Silfer:
  - tirando outras atualizações muito importante para facilitar o trabalho dos ADM e melhorar todo o sistema pra vocês, nós estamos constantemente atualizando o bot, mesmo que vocês não vejam :)
        ''')

      if text.split()[0] == '/sugestao':
        if text == '/sugestao':
          mensagem('use o comando da seguinte forma:\n/sugestao\nentão escreva sua sugestão depois do comando, ex:\n/sugestao faça mais comandos')
        else:
          while True:
            try:
              get(f"{link}sendMessage?chat_id=-838544237&text=sugestão: {text[9:]}")
              break
            except:
              pass
          mensagem('sugeatão enviada!')

      if text.split()[0] in '/ajudaADM':
        if text == '/ajudaADM':
          mensagem('use o comando da seguinte forma:\n/ajudaADM\nentão escreva a ajuda depois do comando, ex:\n/ajudaADM span no grupo vip!')
        else:
          while True:
            try:
              get(f"{link}sendMessage?chat_id=-838544237&text=ajuda: {text[9:]}")
              break
            except:
              pass
          mensagem('ajuda enviada!')

      return True

  def atualizador():
    global jogos, stop2
    sleep(1)
    while True:
      if stop2 == True:
        break
      ouve()
      if verifica_mudanca():
        jogos = pega_lista()
        verifica_estrategias()

  def verifica_mudanca():
    global jogos
    while True:
      ouve()
      if jogos == pega_lista():
        sleep(1)
        continue
      else:
        return True

  def pega_lista():
    while True:
      try:
        lista = []
        r = get('https://blaze.com/api/roulette_games/recent')
        for jogada in r.json():
          lista.append({'cor': jogada['color'], 'numero': jogada['roll']})
        return lista
      except:
        continue

  def acertividade(chave, n):
    global logs

    verifica_hora()

    x = logs[chave][n]['green'] + logs[chave][n]['green branca'] + logs[chave][n]['red']
    logs[chave][n]['acertividade'] = round((logs[chave][n]['green'] + logs[chave][n]['green branca']) * 100 / x, 2)

  def retorna_acertivividade(chave, n):
    global logs

    if logs[chave][n]['green'] + logs[chave][n]['green branca'] + logs[chave][n]['red'] == 0:
      parc_estr = '0%'
    else:
      x = logs[chave][n]['green'] + logs[chave][n]['green branca'] + logs[chave][n]['red']
      parc_estr = f"{(logs[chave][n]['green'] + logs[chave][n]['green branca']) * 100 / x:.2f}%"

    return f"{parc_estr}"

  def numero_estrategia(chave, n):
    p = 0
    for x in enumerate(logs):
      if chave == x[1]:
        return (x[0] + 1 + p) if n == 1 else (x[0] + 2 + p)
      else:
        p+=1

  def retorna_parcial():
    global logs
    global idParcial

    if idParcial:
      while True:
        try:
          get(f'https://api.telegram.org/bot{token}/deleteMessage?chat_id={chat}&message_id={idParcial}')
          idParcial = None
          break
        except:
          pass

    parcial = {'green': 0, 'greenb': 0, 'loss': 0}

    for dado in logs.values():

      # adicionado
      dados1 = dado[1]
      dados2 = dado[2]
      if dados1['acertividade'] > dados2['acertividade']:
        dados = dados1
      else:
        dados = dados2

      # \/ removido (apenas essa primeira linha de baixo)
      #for dados in dado.values():
      if dados['acertividade'] >= 80 and dados['green'] + dados['green branca'] + dados['red'] >= 10:
        parcial['green'] += dados['green']
        parcial['greenb'] += dados['green branca']
        parcial['loss'] += dados['red']

    if parcial["green"] + parcial['greenb'] + parcial['loss'] != 0:
      try:
        porc_parcial = ((parcial["green"] + parcial['greenb']) * 100) / (parcial["green"] + parcial['greenb'] + parcial['loss'])
        str_parcial = f'Parcial ✅ = {parcial["green"]} ⛔️ = {parcial["loss"]} ⚪️ = {parcial["greenb"]}\n🎯 {porc_parcial:.2f}% de acerto'
        return str_parcial
      except:
        pass
    else:
      return 'parcial zerado, nenhum dado resgatado. Tente mais tarde'

  def entrada(aposta, cor, chave, n):
    global jogos
    global token
    global grupo
    global stickers
    global idParcial
    global parcial_hora

    str_aposta = None

    if 'v' in aposta:
      str_aposta = 'vermelha 🔴'
    elif 'p' in aposta:
      str_aposta = 'preta ⚫️'
    elif 'o' in aposta:
      str_aposta = 'vermelha 🔴' if cor == 2 else 'preta ⚫️'
    elif 'i' in aposta:
      str_aposta = 'vermelha 🔴' if cor == 1 else 'preta ⚫️'

    if 'b' in aposta:
      str_aposta2 = 'proteja branco ⚪️'
    else:
      str_aposta2 = None

    if logs[chave][n]['acertividade'] >= 80 and quantidades_jogadas(chave, n) >= 10:
      manda_msg(f'⚠️ entrada confirmada ⚠️\n🏹 estratégia nº: {numero_estrategia(str(chave), n)} 🏹\n🍀 acertividade: {retorna_acertivividade(chave, n)} 🍀\n✅ = {logs[chave][n]["green"]} ⚪️ = {logs[chave][n]["green branca"]} ⛔️ = {logs[chave][n]["red"]}\napostar na cor {str_aposta}\n{f"sugestão: {str_aposta2}" if str_aposta2 else ""}')
      manda_msg(f'[💻 Clique Aqui Para Apostar!!!](https://blaze.com/pt/games/double)&disable_web_page_preview=true&parse_mode=MarkdownV2')

    gale = 0
    green = False
    gales = []
    while True:
      if verifica_mudanca() == True:
        jogos = pega_lista()

        if 'b' in aposta and jogos[0]['cor'] == 0:
          green = True
          logs[chave][n]['green branca'] += 1

        elif 'v' in aposta and jogos[0]['cor'] == 1:
          green = True
          logs[chave][n]['green'] += 1

        elif 'p' in aposta and jogos[0]['cor'] == 2:
          green = True
          logs[chave][n]['green'] += 1

        elif 'o' in aposta and jogos[0]['cor'] != 0 and jogos[0]['cor'] != cor:
          green = True
          logs[chave][n]['green'] += 1

        elif 'i' in aposta and jogos[0]['cor'] != 0 and jogos[0]['cor'] == cor:
          green = True
          logs[chave][n]['green'] += 1

        if green == True:
          if jogos[0]['cor'] == 0:
            if logs[chave][n]['acertividade'] >= 80 and quantidades_jogadas(chave, n) >= 11:
              manda_sticker(stickers['green branco'])
              r = manda_msg(retorna_parcial())
              idParcial = str(r[0]['result']['message_id'])
              parcial_hora['green branca'] += 1
            # manda_msg('🍀💸✅ green branco ✅💸🍀')
          else:
            if logs[chave][n]['acertividade'] >= 80 and quantidades_jogadas(chave, n) >= 11:
              manda_sticker(stickers['green'])
              r = manda_msg(retorna_parcial())
              idParcial = str(r[0]['result']['message_id'])
              parcial_hora['green'] += 1
            # manda_msg('🍀💸✅ green ✅💸🍀')

          acert = logs[chave][n]['acertividade']
          acertividade(chave, n)
          # mudar aqui ainda !!!!!!!!!!!!

          for chat in grupo:
            for id_msg in gales:
              while True:
                try:
                  get(f'https://api.telegram.org/bot{token}/deleteMessage?chat_id={chat}&message_id={id_msg}')
                  break
                except:
                  pass

          break
        else:
          if gale == 1:
            if logs[chave][n]['acertividade'] >= 80 and quantidades_jogadas(chave, n) >= 10:
              manda_sticker(stickers['loss'])
              r = manda_msg(retorna_parcial())
              idParcial = str(r[0]['result']['message_id'])
              parcial_hora['red'] += 1
            # manda_msg('⛔️ red ⛔️')
            logs[chave][n]['red'] += 1

            acert = logs[chave][n]['acertividade']
            acertividade(chave, n)
            if (acert >= 80 and logs[chave][n]['acertividade'] < 80 and quantidades_jogadas(chave, n) >= 11) or (acert == 0 and logs[chave][n]['acertividade'] and logs[chave][n]['red'] != 0 and quantidades_jogadas(chave, n) >= 11):
              manda_msg(f'🔅 estratégia {numero_estrategia(chave, n)} retirada por acertividade muito baixa 🔅')

            verifica_estrategias()

            for chat in grupo:
              for id_msg in gales:
                while True:
                  try:
                    get(f'https://api.telegram.org/bot{token}/deleteMessage?chat_id={chat}&message_id={id_msg}')
                    break
                  except:
                    pass

            break
          else:
            gale += 1
            if logs[chave][n]['acertividade'] >= 80 and quantidades_jogadas(chave, n) >= 10:
              while True:
                try:
                  r = manda_msg(f'🔅 sugerimos entrar no {gale}º gale (opcional) 🔅')
                  break
                except:
                  pass
              gales.append(str(r[0]['result']['message_id']))

  def verifica_estrategias():
    global estrategias
    global jogos
    c1 = None
    c2 = None
    detec = True

    for estrategia in estrategias:
      estrategia['sequencia'].reverse()

      for x in zip(estrategia['sequencia'], jogos):

        if x[0] in ['c1', 'c2']:

          if x[0] == 'c1':
            if c1 == None:
              if x[1]['cor'] != 0:
                if c2 != x[1]['cor']:
                  c1 = x[1]['cor']
                else:
                  detec = False
                  break    
              else:
                detec = False
                break
            else:
              if c1 != x[1]['cor']:
                detec = False
                break
              elif c1 == x[1]['cor']:
                continue

          elif x[0] == 'c2':
            if c2 == None:
              if x[1]['cor'] != 0:
                if c1 != x[1]['cor']:
                  c2 = x[1]['cor']
                else:
                  detec = False
                  break
              else:
                detec = False
                break
            else:
              if c2 != x[1]['cor']:
                detec = False
                break
              elif c2 == x[1]['cor']:
                continue

        elif x[0] in ['v', 'p', 'q', 'b']:

          if x[0] == 'v' and x[1]['cor'] == 1:
            continue
          elif x[0] == 'p' and x[1]['cor'] == 2:
            continue
          elif x[0] == 'q':
            continue
          elif x[0] == 'b' and x[1]['cor'] == 0:
            continue
          else:
            detec = False
            break

        elif x[0] in [*range(1, 15)]:
          if x[0] == x[1]['numero']:
            continue
          else:
            detec = False
            break

      estrategia['sequencia'].reverse()

      if detec == True:
        cor = None
        if estrategia['sequencia'][-1] == 'b':
          if estrategia['sequencia'][-2] == 'b':
            cor = c1 if estrategia['sequencia'][-3] == 'c1' else c2
          else:
            cor = c1 if estrategia['sequencia'][-2] == 'c1' else c2
        else:
          cor = c1 if estrategia['sequencia'][-1] == 'c1' else c2

        # função pra determinar qual cor vai apostar !!!!!!!!!!!!!!!!!!!!!

        estr = logs[str(estrategia['sequencia'])]

        def calc(n):
          return estr[n]['green'] + estr[n]['green branca'] * 2 - estr[n]['red'] * 5

        if calc(1) > calc(2):
          tipo_escolhido = 1
        elif calc(1) < calc(2):
          tipo_escolhido = 2
        elif calc(1) == calc(2):
          tipo_escolhido = 1

        for estrategia2 in estrategias:
          if estrategia2['sequencia'] == estrategia['sequencia'] and estrategia2['tipo'] == tipo_escolhido:
            aposta_escolhida = estrategia2['aposta']

        entrada(aposta_escolhida, cor, str(estrategia['sequencia']), tipo_escolhido)
        break

      else:
        c1 = None
        c2 = None
        detec = True

  ouve()
  print('bot iniciado!')
  manda_msg('bot iniciado!')
  atualizador()

except Exception as error:
  while True:
    try:
      get(f"{link}sendMessage?chat_id=5027889205&text=erro encontrado no grupo vip:\n{error}\n\nreiniciando o bot").json()
      break
    except:
      pass
