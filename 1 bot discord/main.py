# feito para ser um codigo de simulação de carteiras individuais para cada membro do servidor, alem de poderem comprar cargos com o bot, podendo, com a confirmação do dono, resetar e recriar toda a economia, com os administradores sendo responsaveis por espalharem o dinheiro e criar os itens(onde iria conter os cargos)

from decouple import config
import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument
import tracemalloc
from github import Github
from os import remove

tracemalloc.start() # usado para poder rastrear uma variavel até onde está armazenada

# pega a db do github e tras pra aplicação
token = 'token do git'
mainrepo = 'nome do repositório'
indice = 'inteiro, indice da db'
git = Github(token)

def pegadb():
  return eval(git.get_user().get_repo(mainrepo).get_contents('/')[indice].decoded_content.decode('utf-8'))

async def escrevedb(db):
  repo = git.get_user().get_repo(mainrepo)
  contents = repo.get_contents('/')[indice]
  repo.update_file(contents.path, "", str(db), contents.sha)

db = pegadb()

# do bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!pp ', intents=intents, help_command=None)

# de comando
liberarResetEconomy = False
liberado = False

# de cargo
testeBot = 'id do cargo que testa os bot'
moderador = 'id do cargo de moderador'
membroAtivo = 'id od cargo de mebro ativo'

# de usuario
dono = 'id do dono'
meuId = 'seu id'

# de canal
canalNomeTeste = 'teste-bot'
logBot = int(db['log'])
comandos = db['comandos']

# de server
nome_do_server_disponivel1 = 'id do servidor'
servers = [nome_do_server_disponivel1] # lista dos servidores disponiveis

# funções ----------------------------------------------------------------------------------------

async def canal(message): # para saber se o canal de resposta é o de teste
  return True if message.channel.name == canalNomeTeste or message.channel.id == comandos else False

async def guild(message): # verifica se o servidor é valido
  if message.guild.id in servers:
    return True
  else:
    return False

async def cargos(message): #retorna uma lista dos cargos do author da mensagem
  lista = [] 
  for cargo in message.author.roles:
    lista.append(cargo.id)
  return lista

async def pegaid(mensao): # pega o id do membro mensionado
  return f'{mensao[3:-1]}'

async def criacarteira(message):
  db[str(message.author.id)] = {'pp':0, 'itens':{}}

async def envialog(message, titulo, descricao):
  embed=discord.Embed(title=titulo, description=descricao, color=0x88c5cc)
  embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/941112607467778071/944671714464370748/bottestimg2.png')
  await message.guild.get_channel(logBot).send(embed=embed)

# eventos ----------------------------------------------------------

@bot.event # para saber quando o bot está pronto
async def on_ready():
  global db
  if not 'loja' in db.keys():
    db['loja'] = {}
    await escrevedb(db)
  print(f'estou logado no {bot.user.name}')

@bot.event # para adicionar uma carteira a um usuario que entrou
async def on_member_join(membro):
  global db
  db[str(membro.id)] = {'pp':0,'itens':{}}
  await escrevedb(db)
  await envialog(membro, 'CARTEIRA CRIADA', f'carteira criada para {membro.mention}\nuse !pp para ver os comandos')

@bot.event # para deletar a carteira do usuario que saiu
async def on_member_remove(membro):
  global db
  del db[str(membro.id)]
  await escrevedb(db)
  await envialog(membro, 'CARTEIRA DELETADA', f'carteira de {membro.mention} deletada')

@bot.event # para quando der algum erro na api do discord
async def on_command_error(message, error):
  if isinstance(error, MissingRequiredArgument):
    await message.channel.send(f'faltando argumentos no comando, use (!pp help comando) para ver os dados do comando')
  elif isinstance(error, CommandNotFound):
    await message.channel.send('comando não encontrado, use !pp help para ver todos os comandos')
  else:
    raise error

@bot.event # para o bot n responder a ele mesmo
async def on_message(message):
  global logBot
  global comandos
  global db

  async def commands(message):
    await bot.process_commands(message)
    await escrevedb(db)

  if message.author == bot.user:
    pass

  elif await guild(message):
    if await canal(message) and await guild(message):
      logBot = int(db['log'])
      comandos = db['comandos']

      mensagem = str(message.content)

      if '!pp' in mensagem:
        if mensagem.index('!pp') == 0:
          if len(mensagem) > 3:
            if message.content[4] == ' ':
              await help(message)
            else:
              await commands(message)
          elif len(mensagem) == 3:
              await help(message)
          else:
            await commands(message)
        else:
          await commands(message)
      else:
        await commands(message)

      logBot = int(db['log'])
      comandos = db['comandos']
    else:
      if message.content.startswith('!pp'):
        await message.channel.send(f'o bot {bot.user.name} não está disponivel nesse canal, so no canal {message.guild.get_channel(comandos).mention} ou em qualquer canal com o nome teste-bot')
  else:
    if message.content.startswith('!pp'):
      await message.channel.send(f'o bot {bot.user.name} não está disponivel para o seu servidor, contate Purple-Senpai#2860 para libera-lo')

# comandos livres -------------------------------------------------------------------------

@bot.command()
async def help(message): # comando help para usuarios comuns
  embed=discord.Embed(title="HELP", description="Todos os comandos do InvitedBOT", color=0x88c5cc)

  embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/941112607467778071/944671714464370748/bottestimg2.png')

  embed.add_field(name="**teste**", value='''**!pp teste**
Testa conexão com o bot
Se a mensagem for respondida, então o bot está online, caso contrário o bot está offline.
''', inline=False)

  embed.add_field(name="**carteira**", value='''**!pp carteira** Para ver sua carteira
Vê dinheiro e itens da carteira
**!pp carteira @membro** Para ver a carteira de outra pessoa.
Usado para ver o pp e itens da sua ou da carteira de outra pessoa.''', inline=False)

  embed.add_field(name='**loja**', value='''**!pp loja**
Visualiza os itens da loja.
Mostra os itens a venda, do mais antigo ao mais novo
Mostra um contador, nome do item, preço e se é empilhavel.''', inline=False)

  embed.add_field(name="**iteminfo**", value='''**!pp iteminfo nomedoitem**
Mostra todas as informações de um item do seu inventario ou da loja
Não mostrará informações se o item estiver somente no inventario de outro membro.
O nome do item é obrigatório.''', inline=False)

  embed.add_field(name="**compraritem**", value='''**!pp compraritem nomedoitem quantidade**
Usado para comprar um item da loja.
Seu pp será subtraído de acordo com o preço do item multiplicado pela quantidade.
Se você não possuir pp suficiente, o item não será comprado.
Se não tiver dada a quantidade, sera comprado apenas uma vez
O nome do item é obrigatório.''', inline=False)

  embed.add_field(name="**usaritem**", value='''**!pp usaritem nomedoitem**
Usa um item do seu inventario
Quando usado, você ganhará o cargo do item.
O item sera deletado do seu inventário depois o uso.
O nome do item é obrigatório.''', inline=False)

  embed.add_field(name="**rankingpp**", value='''**!pp rankingpp**
Mostra o top 10 dos usuarios com mais pp
Os usuários com 0pp não serão mencionados.
Caso todos tenham 0pp, ninguém será mencionado.''', inline=False)

  embed.set_footer(text="""!pp help - essa mensagem que você está vendo
!pp helpa - para comandos de membros ativos
!pp helpm - para comandos de moderadores
!pp helpd - para comandos de dono""")

  await message.channel.send(embed=embed)

@bot.command()
async def helpa(message): # comando help para usuarios ativos
  embed=discord.Embed(title="HELP", description="Todos os comandos do InvitedBOT", color=0x88c5cc)

  embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/941112607467778071/944671714464370748/bottestimg2.png')

  embed.add_field(name="**givepp**", value='''**!pp givepp quantia @membro**
Dá  seu pp para outro membro
O pp é retirado da sua carteira e enviado para a carteira do membro mencionado.
A quantidade e a menção são obrigatórias.''', inline=False)

  embed.set_footer(text="""!pp help - para comandos livres
!pp helpa - para comandos de essa mensagem que você está vendo
!pp helpm - para comandos de moderadores
!pp helpd - para comandos de dono""")

  await message.channel.send(embed=embed)

@bot.command()
async def helpm(message): # comando help para moderadores
  embed=discord.Embed(title="HELP", description="Todos os comandos do InvitedBOT", color=0x88c5cc)

  embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/941112607467778071/944671714464370748/bottestimg2.png')

  embed.add_field(name="**comandpp**", value=f'''**!pp comandpp #novochat**
Muda onde os comandos são recebidos.
O chat de {message.guild.get_channel(db['comandos']).mention} é onde os comandos serão recebidos e executados, caso você coloque um chat que não existe, pode acabar impossibilitando o bot de funcionar.''', inline=False)

  embed.add_field(name="**daritem**", value='''**!pp daritem nomedoitem @membro**
Dá um item a um membro
Pode transferir um item do seu inventario para o de outro membro.
O item irá sumir do seu inventário.
Argumentos: nomeitem e menção são obrigatórios.''', inline=False)

  embed.add_field(name="**auditpp**", value='''**!pp auditpp #novocanal** para mudar o canal de log.
Muda o log de auditoria do bot
**!pp auditpp** para ver o canal usado
O log são mensagens de criação e remoção de carteiras.''', inline=False)

  embed.add_field(name="**resetpp**", value='''**!pp resetpp** Para resetar o dinheiro da sua carteira.
Reseta o dinheiro da carteira
**!pp resetpp @mençao** Para resetar o pp da carteira de alguém.
Zera o pp da sua ou da carteira de alguém, sem remover os itens.''', inline=False)

  embed.add_field(name="**delpp**", value='''**!pp delpp Quantia** para remover o pp da sua carteira.
Remove pp da carteira.
**!pp delpp quantia @mençao** Para remover o pp da carteira de outro membro.
Remove a quantia argumentada da carteira escolhida, não deixando o pp ficar menor que 0.
Escrever a quantia é obrigatório.''', inline=False)

  embed.add_field(name="**addpp**", value='''**!pp addpp quantia** Para adicionar dinheiro a sua carteira.
Adiciona dinheiro a carteira
**!pp addpp quantia @mençao** Para adicionar dinheiro a carteira de alguém.
Soma o pp da carteira selecionada com a quantia desejada.
Escrever a quantia é obrigatório.''', inline=False)

  embed.add_field(name="**delitem**", value='''**!pp delitem nomedoitem**
Deleta um item dentro do mercado
Deleta apenas o item do mercado, não deletará o item do inventario de outras pessoas.
Caso o item seja usado e o cargo já não existir, o pp será reembolsado e o item deletado.
Escrever o nome do item é obrigatório.''', inline=False)

  embed.add_field(name="**edititem**", value='''**!pp edititem nomedoitem novonome novopreco @novocargo empilhavel**
Edita um item dentro da loja
Caso não quiser mudar uma das opções é só usar none, ex:
**!pp edititem nomedoitem none 50 none, por exemplo**
Na opção empilhavel, coloque 'sim' para ser empilhavel e 'nao' para não ser empilhavel.
Escrever o nome do item é obrigatório.''', inline=False)

  embed.add_field(name="**criaritem**", value='''**!pp criaritem nomedoitem precodoitem @cargo empilhavel**
Cria um item para a loja
ex: **!pp criaritem item1 100 @cargo** para criar um item com nome item1, preço 100 e cargo @cargo que não seja acomulativo
ex: **!pp criaritem item1 100 @cargo empilhavel** para criar um item com nome item1, preço 100 e cargo @cargo que é acomulativo
Todos os argumentos acima são obrigatórios.''', inline=False)

  embed.set_footer(text="""!pp help - para comandos livres
!pp helpa - para comandos de membros ativos
!pp helpm - para comandos de essa mensagem que você está vendo
!pp helpd - para comandos de dono""")

  await message.channel.send(embed=embed)

@bot.command()
async def helpd(message): # comando help para dono
  embed=discord.Embed(title="HELP", description="Todos os comandos do InvitedBOT", color=0x000000)
  
  embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/941112607467778071/944671714464370748/bottestimg2.png')

  embed.add_field(name="**resetallwalletsforeveyone**", value='''**!pp resetallwalletsforeveyone** Só pode ser usado pelo Dono
Reinicia a economia.
Para usar o comando, é necessario usá-lo, usar o comando de confirmação (!pp confirm) e usá-lo novamente.''', inline=False)

  embed.add_field(name="**confirm**", value='''!pp confirm Confirma o comando !pp resetallwalletsforeveyone.
Comando de confirmação''', inline=False)

  embed.set_footer(text="""!pp help - para comandos livres
!pp helpa - para comandos de membros ativos
!pp helpm - para comandos de moderadores
!pp helpd - para comandos de essa mensagem que você está vendo""")

  await message.channel.send(embed=embed)

# comandos de teste \/

@bot.command()
async def helpt(message):
  if int(meuId) == int(message.author.id):
    embed=discord.Embed(title="HELP TESTER", description="Comandos de teste do InvitedBOT", color=0x000000)

    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/941112607467778071/944671714464370748/bottestimg2.png')

    embed.add_field(name="**backupDB**", value='''**!pp backupDB** usado para criar uma cópia do banco de dados
    a cópia será enviada para o privado do usuário que usar o comando.''', inline=False)

    embed.add_field(name="**uploadDB**", value='''**!pp uploadDB <arquivo>** usado para fazer upload de um banco de dados existente para o do bot
    comando sensível, podendo impossibilitar o funcionamento do bot.''', inline=False)
    
    embed.add_field(name="**emergencyRepairDB**", value='''**!pp emergencyRepairDB** caso aconteça algum erro no upload, ou o arquivo errado seja enviado, esse comando tentará consertar a base de dados.''', inline=False)

    embed.add_field(name="**totalpp**", value='''**!pp totalpp** mostrará o total de pp em criculação no servidor.''', inline=False)
  else:
    embed=discord.Embed(title='você não pode usar comandos de teste!.', color=0x000000)

  await message.channel.send(embed=embed)

@bot.command()
async def totalpp(message):
  if int(meuId) == int(message.author.id):
    total = 0
    for chave in db:
      if chave in ['loja', 'log', 'comandos']:
        pass
      else:
        if db[chave]['pp'] != 0:
          total += db[chave]['pp']
    embed=discord.Embed(title=f'{total}pp em circulação no servidor.', color=0x000000)
  else:
    embed=discord.Embed(title='você não pode usar esse comando!.', color=0x000000)
  await message.channel.send(embed=embed)

@bot.command()
async def backupDB(message):
  if int(meuId) == int(message.author.id):
    embed=discord.Embed(title='Enviando o banco de dados para seu privado.', color=0x000000)
    arquivo = open('db.txt', 'w')
    arquivo.write(str(db))
    arquivo.close()
    await message.author.send(file=discord.File('db.txt'))
    remove('db.txt')
    await envialog(message, 'LOG ENVIADO', f'{message.author.mention} salvou o banco de dados no seu privado.')
  else:
    embed=discord.Embed(title='você não pode usar comandos de teste!.', color=0x000000)
  await message.channel.send(embed=embed)

@bot.command()
async def uploadDB(message):
  global db
  if int(meuId) == int(message.author.id):
    try:
      txt = await message.message.attachments[0].read()
      txt = txt.decode('utf-8')
      db = eval(txt)
      embed=discord.Embed(title='Banco de dados carregado com sucesso!.', color=0x000000)
      await envialog(message, 'UPLOAD DB', f'{message.author.mention} fez upload de um banco de dados.')
    except IndexError:
      embed=discord.Embed(title='Nenhum arquivo encontrado.', color=0x000000)
    except UnicodeDecodeError:
      embed=discord.Embed(title='Arquivo não é um texto.', color=0x000000)
  else:
    embed=discord.Embed(title='você não pode usar comandos de teste!.', color=0x000000)
  await message.channel.send(embed=embed)

@bot.command()
async def emergencyRepairDB(message):
  global db
  if int(meuId) == int(message.author.id):
    db = {'log': None, 'loja': {}, 'comandos': None}
    embed=discord.Embed(title='base de dados formatada, use um canal nomeado de "teste-bot" para reconfigurar o bot ou contate o programador.', color=0x000000)
    await envialog(message, 'FORMATAÇÃO DE EMERGENCIA', f'{message.author.mention} formato o banco de dados.')
  else:
    embed=discord.Embed(title='você não pode usar comandos de teste!.', color=0x000000)
  await message.channel.send(embed=embed)

@bot.command()
async def teste(message):# comando teste
  embed=discord.Embed(title="teste efetuado", description=f"mensagem recebida de {message.author.name}.", color=0xffffff)
  await message.channel.send(embed=embed)

# comandos de teste /\

@bot.command()
async def carteira(message, mensao=None): # para ver sua carteira

  embed=discord.Embed(title="CARTEIRA", description="dinheiro e itens", color=0x3da560)
  embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/941112607467778071/944626931343708180/1645051599232.png')

  global db
  if mensao == None:
    if not str(message.author.id) in db.keys():
      await criacarteira(message)
    embed.add_field(name="**dinheiro**", value=f'você tem {db[str(message.author.id)]["pp"]}PP na sua carteira.', inline=False)
    if len(db[str(message.author.id)]['itens']) == 0:
      embed.add_field(name="**itens**", value='você ainda não comprou nenhum item', inline=False)
    else:
      itens = ''
      if len(db[str(message.author.id)]['itens'].keys()) == 1:
        for item in db[str(message.author.id)]['itens'].keys():
          if 'quantidade' in db[str(message.author.id)]['itens'][item].keys():
            quantidade = db[str(message.author.id)]['itens'][item]['quantidade']
          else:
            quantidade = 1
          itens += f'{f"{quantidade} " if quantidade > 1 else ""}{item}'
        embed.add_field(name="**itens**", value=f'você já comprou o item: {itens}', inline=False)
      else:
        for item in db[str(message.author.id)]['itens'].keys():
          if 'quantidade' in db[str(message.author.id)]['itens'][item].keys():
            quantidade = db[str(message.author.id)]['itens'][item]['quantidade']
          else:
            quantidade = 1
          itens += f'{f"{quantidade} " if quantidade > 1 else ""}{item}, '
        embed.add_field(name="**itens**", value=f'você já comprou os itens: {itens[:-2]}', inline=False)
  else:
    idMensao = await pegaid(mensao)
    if idMensao in db.keys():
      embed.add_field(name="**dinheiro**", value=f'{mensao} tem {db[str(idMensao)]["pp"]}PP na carteira', inline=False)
      if len(db[str(idMensao)]['itens']) == 0:
        embed.add_field(name="**itens**", value=f'{mensao} ainda não comprou nenhum item.', inline=False)
      else:
        itens = ''
        for item in db[str(idMensao)]['itens'].keys():
          if 'quantidade' in db[str(idMensao)]['itens'][item].keys():
            quantidade = db[str(idMensao)]['itens'][item]['quantidade']
          else:
            quantidade = 1
          itens += f'{f"{quantidade} " if quantidade > 1 else ""}{item}, '
        embed.add_field(name="**itens**", value=f'{mensao} ja comprou os itens: {itens[:-2]}', inline=False)
    else: # melhorar posteriormente a forma de detecção de usuario inesistente !!!!
      embed.add_field(name="**usuario inesistente**", value=f'{mensao}!, use !pp carteira para criar sua carteira', inline=False)
  await message.channel.send(embed=embed)

@bot.command()
async def loja(message): # para ver a loja
  embed=discord.Embed(title="Loja", description="itens a venda", color=0xcc4145)
  embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/941839920824213525/944668198706495529/bot1img.png')
  global db
  if not 'loja' in db.keys():
    db['loja'] = {}
  else:
    if len(db['loja']) == 0:
      embed.add_field(name="**itens**", value='nenhum item esta a venda na loja.', inline=False)
    else:
      texto = ''
      for item in db['loja']:
        embed.add_field(name=f"**nome**", value=f'{item}', inline=True)
        for chave in db['loja'][item].keys():
          if chave == 'quantidade':
            embed.add_field(name=f"**empilhamento**", value='ativado', inline=False)
          else:
            embed.add_field(name=f"**{chave}**", value=f'{message.guild.get_role(db["loja"][item][chave]).mention if chave == "cargo" else db["loja"][item][chave]}', inline=True)
  await message.channel.send(embed=embed)

@bot.command()
async def iteminfo(message, nomeitem): # para ver as informações de um item
  embed=discord.Embed(title="INFORMAÇÕES DO ITEM", description="informações do item da loja ou do seu iventario", color=0x3da560)
  global db
  if nomeitem in db['loja'].keys():
    embed.add_field(name=f"**nome**", value=f'{nomeitem}', inline=True)
    embed.add_field(name=f"**preço**", value=f'{db["loja"][nomeitem]["preco"]}PP', inline=True)
    embed.add_field(name=f"**cargo**", value=f'{message.guild.get_role(db["loja"][nomeitem]["cargo"]).mention}', inline=True)
    embed.add_field(name=f"**empilhavel**", value=f'{"sim" if "quantidade" in db["loja"][nomeitem].keys() else "não"}', inline=True)
  elif nomeitem in db[str(message.author.id)]["itens"].keys():
    embed.add_field(name=f"**nome**", value=f'{nomeitem}', inline=True)
    embed.add_field(name=f"**preço**", value=f'{db[str(message.author.id)]["itens"][nomeitem]["preco"]}PP', inline=True)
    embed.add_field(name=f"**cargo**", value=f'{message.guild.get_role(db[str(message.author.id)]["itens"][nomeitem]["cargo"]).mention}', inline=True)
    embed.add_field(name=f"**empilhavel**", value=f'{"sim" if "quantidade" in db[str(message.author.id)]["itens"][nomeitem].keys() else "não"}', inline=True)
  else:
    embed.add_field(name=f"**{nomeitem}**", value=f'item não encontrado', inline=False)
  await message.channel.send(embed=embed)

@bot.command()
async def compraritem(message, nomeitem, quantidade=None): # para comprar um item
  try:
    global db
    if not str(message.author.id) in db.keys():
      await criacarteira(message)
    if not nomeitem in db['loja'].keys():
      embed=discord.Embed(title='item não encontrado.', color=0xdd0808)
    elif db[str(message.author.id)]['pp'] < db['loja'][nomeitem]['preco']:
      embed=discord.Embed(title='você não tem dinheiro suficiente.', color=0x3da560)
    elif quantidade != None and quantidade.isnumeric() and db[str(message.author.id)]['pp'] < db['loja'][nomeitem]['preco'] * int(quantidade):
      embed=discord.Embed(title='você não tem dinheiro suficiente.', color=0x3da560)
    else:
      quantidade = int(quantidade) if quantidade != None and quantidade.isnumeric() else 1
      if nomeitem in db[str(message.author.id)]['itens'].keys():
        if 'quantidade' in db[str(message.author.id)]['itens'][nomeitem].keys():
          db[str(message.author.id)]['itens'][nomeitem]['quantidade'] += 1 * quantidade if quantidade != None else 1
          db[str(message.author.id)]['pp'] -= db['loja'][nomeitem]['preco'] * quantidade if quantidade != None else 1
          embed=discord.Embed(title='item comprado.', color=0x3da560)
          await envialog(message, 'ITEM COMPRADO', f'{message.author.mention} comprou {quantidade if quantidade != None else 1} vez e acomulou o item {nomeitem} da loja')
        else:
          embed=discord.Embed(title='esse item não é acomulativo, você não pode comprar outro.', color=0x3da560)
      else:
        if 'quantidade' in db['loja'][nomeitem].keys():
          db[str(message.author.id)]['itens'][nomeitem] = db['loja'][nomeitem].copy()
          db[str(message.author.id)]['itens'][nomeitem]['quantidade'] = quantidade
          db[str(message.author.id)]['pp'] -= db['loja'][nomeitem]['preco'] * quantidade if quantidade != None else 1
          embed=discord.Embed(title='item comprado.', color=0x3da560)
          await envialog(message, 'ITEM COMPRADO', f'{message.author.mention} comprou {quantidade if quantidade != None else 1} vez e acomulou o item {nomeitem} da loja')
        else:
          db[str(message.author.id)]['pp'] -= db['loja'][nomeitem]['preco']
          db[str(message.author.id)]['itens'][nomeitem] = db['loja'][nomeitem].copy()
          embed=discord.Embed(title='item comprado.', color=0x3da560)
          await envialog(message, 'ITEM COMPRADO', f'{message.author.mention} comprou o item {nomeitem} da loja')
    await message.channel.send(embed=embed)
  except ValueError:
    embed=discord.Embed(title='use numeros inteiros na quantidade desejada de compra.', color=0xdd0808)
    await message.channel.send(embed=embed)

@bot.command()
async def usaritem(message, nomeitem): # para usar um item
  global db
  if not str(message.author.id) in db.keys():
    await criacarteira(message)
  if not nomeitem in db[str(message.author.id)]['itens'].keys():
    embed=discord.Embed(title='item não encontrado na sua carteira.', color=0xdd0808)
  else:
    try:
      membro = message.guild.get_member(message.author.id)
      role = message.guild.get_role(db[str(message.author.id)]['itens'][nomeitem]['cargo'])
      try:
        await membro.add_roles(role)
      except:
        pass
      if nomeitem in db['loja'].keys():
        if 'quantidade' in db[str(message.author.id)]['itens'][nomeitem].keys():
          if db[str(message.author.id)]['itens'][nomeitem]['quantidade'] > 1:
            db[str(message.author.id)]['itens'][nomeitem]['quantidade'] -= 1
            embed=discord.Embed(title='item usado.', color=0x3da560)
            await envialog(message, 'ITEM USADO', f'{message.author.mention} usou o item {nomeitem} e ganhou o cargo {role.mention}')
          else:
            del db[str(message.author.id)]['itens'][nomeitem]
            embed=discord.Embed(title='item usado.', color=0x3da560)
            await envialog(message, 'ITEM USADO', f'{message.author.mention} usou o item {nomeitem} e ganhou o cargo {role.mention}')
        else:
          del db[str(message.author.id)]['itens'][nomeitem]
          embed=discord.Embed(title='item usado.', color=0x3da560)
          await envialog(message, 'ITEM USADO', f'{message.author.mention} usou o item {nomeitem} e ganhou o cargo {role.mention}')
      else:
        embed=discord.Embed(title='ouve algum problema.', color=0xdd0808)
        if 'quantidade' in db[str(message.author.id)]['itens'][nomeitem].keys():
          db[str(message.author.id)]['pp'] += int(db[str(message.author.id)]['itens'][nomeitem]['preco']) * int(db[str(message.author.id)]['itens'][nomeitem]['quantidade'])
        else:
          db[str(message.author.id)]['pp'] += db[str(message.author.id)]['itens'][nomeitem]['preco']
        if nomeitem in db['loja'].keys():
          if db[str(message.author.id)]['itens'][nomeitem]['cargo'] == db['loja'][nomeitem]['cargo']:
            del db[str(message.author.id)]['itens'][nomeitem]
            del db['loja'][nomeitem]
            embed.add_field(name=f"**cargo inesistente ou excluido**", value=f'dinheiro devolvido e item excluido.', inline=False)
            await envialog(message, 'ERRO DE USO DE ITEM', f'dinheiro devolvido pro {message.author.mention} do item {nomeitem}, item excluido da loja por cargo inesistente.')
          else:
            del db[str(message.author.id)]['itens'][nomeitem]
            embed.add_field(name=f"**cargo inesistente ou excluido**", value=f'dinheiro devolvido.', inline=False)
            await envialog(message, 'ERRO DE USO DE ITEM', f'dinheiro devolvido pro {message.author.mention} do item {nomeitem} por cargo inesistente, item não excluido da loja pois o cargo não era igual.')
        else:
            del db[str(message.author.id)]['itens'][nomeitem]
            embed.add_field(name=f"**cargo inesistente ou excluido**", value=f'dinheiro devolvido.', inline=False)
            await envialog(message, 'ERRO DE USO DE ITEM', f'dinheiro devolvido pro {message.author.mention} do item {nomeitem} por cargo inesistente, item não foi deletado da loja pois não foi encontrado nela.')
    except:
      embed=discord.Embed(title='ouve algum problema.', color=0xdd0808)
      if 'quantidade' in db[str(message.author.id)]['itens'][nomeitem].keys():
        db[str(message.author.id)]['pp'] += int(db[str(message.author.id)]['itens'][nomeitem]['preco']) * int(db[str(message.author.id)]['itens'][nomeitem]['quantidade'])
      else:
        db[str(message.author.id)]['pp'] += db[str(message.author.id)]['itens'][nomeitem]['preco']
      if nomeitem in db['loja'].keys():
        if db[str(message.author.id)]['itens'][nomeitem]['cargo'] == db['loja'][nomeitem]['cargo']:
          del db[str(message.author.id)]['itens'][nomeitem]
          del db['loja'][nomeitem]
          embed.add_field(name=f"**cargo inesistente ou excluido**", value=f'dinheiro devolvido e item excluido.', inline=False)
          await envialog(message, 'ERRO DE USO DE ITEM', f'dinheiro devolvido pro {message.author.mention} do item {nomeitem}, item excluido da loja por cargo inesistente.')
        else:
          del db[str(message.author.id)]['itens'][nomeitem]
          embed.add_field(name=f"**cargo inesistente ou excluido**", value=f'dinheiro devolvido.', inline=False)
          await envialog(message, 'ERRO DE USO DE ITEM', f'dinheiro devolvido pro {message.author.mention} do item {nomeitem} por cargo inesistente, item não excluido da loja pois o cargo não era igual.')
      else:
          del db[str(message.author.id)]['itens'][nomeitem]
          embed.add_field(name=f"**cargo inesistente ou excluido**", value=f'dinheiro devolvido.', inline=False)
          await envialog(message, 'ERRO DE USO DE ITEM', f'dinheiro devolvido pro {message.author.mention} do item {nomeitem} por cargo inesistente, item não foi deletado da loja pois não foi encontrado nela.')
  await message.channel.send(embed=embed)

@bot.command()
async def rankingpp(message): # para ver o top 10 dos membros com mais dinheiro
  embed=discord.Embed(title='TOP 10 PP.', color=0xffc400)
  embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/941839920824213525/944668327178010685/botimg2.png')
  global db
  dictpp = {}
  listpp = []
  voce = False
  for chave in db.keys():
    if chave == 'loja' or chave == 'log' or chave == 'comandos':
      continue
    else:
      if db[chave]['pp'] == 0:
        pass
      else:
        dictpp[int(chave)] = int(db[chave]['pp'])
  if len(dictpp) == 0:
    embed=discord.Embed(title='todos tem 0PP.', color=0xffc400)
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/941839920824213525/944668327178010685/botimg2.png')
  else:
    for chave in dictpp.keys():
      listpp.append(dictpp[chave]) # int(chave)
    listpp.sort()
    for i in range(10):
      try:
        for chave in dictpp.keys():
          if dictpp[chave] != listpp[-1]:
            continue
          else:
            if chave == message.author.id:
              voce = True
              embed.add_field(name=f"**{i+1}# __{message.guild.get_member(chave).name}__**", value=f'{dictpp[chave]}', inline=False)
              listpp.pop()
              del dictpp[chave]
              break
            else:
              embed.add_field(name=f"**{i+1}# {message.guild.get_member(chave).name}**", value=f'{dictpp[chave]}', inline=False)
              listpp.pop()
              del dictpp[chave]
              break
      except:
        break
    if voce == False:
      embed.set_footer(text=f'você tem: {db[str(message.author.id)]["pp"]}PP')
  await message.channel.send(embed=embed)

# comandos membros ativos -----------------------------------------------------

@bot.command()
async def givepp(message, quantia, mensao): # para dar dinheiro pra outra pessoa
  global db
  if testeBot in await cargos(message) or moderador in await cargos(message) or membroAtivo in await cargos(message) or dono == message.author.id:
    try:
      if not str(message.author.id) in db.keys():
        await criacarteira(message)
      if db[str(message.author.id)]['pp'] < int(quantia):
        embed=discord.Embed(title="não foi possivel dar dinheiro", description="você não tem dinheiro suficiente.", color=0x3da560)
      else:
        quantia = int(quantia)
        db[str(message.author.id)]['pp'] -= quantia
        db[await pegaid(mensao)]['pp'] += quantia
        embed=discord.Embed(title="transferencia efetuada", color=0x3da560)
        await envialog(message, 'DINHEIRO TRANSFERIDO', f'{quantia}pp foi transferido para {mensao} de {message.author.mention}')
    except ValueError:
      embed=discord.Embed(title='valor usado não é um inteiro, use numeros, sem virgulas, sem pontos, sem letras e sem caracteres especieais', color=0xdd0808)
  else:
    embed=discord.Embed(title='você não tem cargo suficiente.', color=0xdd0808)
  await message.channel.send(embed=embed)

# comandos moderadores -------------------------------------------------------

@bot.command()
async def criaritem(message, nome, preco, cargo, quantidade=None): # para criar um item
  global db
  if testeBot in await cargos(message) or moderador in await cargos(message) or dono == message.author.id:
    try:
      if nome in db['loja'].keys():
        embed=discord.Embed(title="esse item já existe na loja.", color=0x3da560)
      else:
        lista = []
        for item in db['loja']:
          lista.append(db['loja'][item]['cargo'])
        if int(f'{cargo[3:-1]}') in lista:
          embed=discord.Embed(title="já existe um item para esse cargo.", color=0x3da560)
        else:
          if quantidade == None or quantidade in ['not', 'no', 'nao', 'não', 'n']:
            db['loja'][nome] = {'preco':int(preco), 'cargo':int(f'{cargo[3:-1]}')}
          else:
            db['loja'][nome] = {'preco':int(preco), 'cargo':int(f'{cargo[3:-1]}'), 'quantidade':1}
          embed=discord.Embed(title=f"item {nome} criado.", color=0x3da560)
    except ValueError:
      embed=discord.Embed(title='valor usado não é um inteiro, use numeros, sem virgulas, sem pontos, sem letras e sem caracteres especieais.', color=0xdd0808)
  else:
    embed=discord.Embed(title='você não tem cargo suficiente.', color=0xdd0808)
  await message.channel.send(embed=embed)

@bot.command()
async def edititem(message, nome, novonome='none', preco='none', cargo='none', quantidade='none'): # para editar um item
  global db
  if moderador in await cargos(message) or testeBot in await cargos(message) or dono == message.author.id:
    try:
      if not nome in db['loja'].keys():
        embed=discord.Embed(title='esse item não existe na loja, use !pp criaritem para criar esse item.', color=0xdd0808)
      else:
        if novonome == 'none' and preco == 'none' and cargo == 'none':
          embed=discord.Embed(title="você escolheu mudar nada.", color=0x3da560)
        else:
          if novonome != 'none':
            if novonome in db['loja'].keys():
              embed=discord.Embed(title="já existe um item com esse nome.", color=0x3da560)
            else:
              db['loja'][novonome] = db['loja'][nome]
              del db['loja'][nome]
              embed.add_field(name=f"**nome**", value='nome modificado', inline=False)
          if preco != 'none':
            db['loja'][nome]['preco'] = int(preco)
            embed.add_field(name=f"**preço**", value='preço modificado', inline=False)
          if cargo != 'none':
            cargo = await pegaid(cargo)
            lista = []
            for item in db['loja']:
              lista.append(db['loja'][item]['cargo'])
            if int(cargo) in lista:
              embed.add_field(name=f"**cargo**", value='já existe um item com esse cargo', inline=False)
            else:
              db['loja'][nome]['cargo'] = int(cargo)
              embed.add_field(name=f"**cargo**", value='cargo modificado', inline=False)
          if quantidade != 'none':
            try:
              if quantidade in ['sim', 's', 'true', 'verdadeiro']: # sla
                db['loja'][nome]['quantidade'] = 1
                embed.add_field(name=f"**quantidade**", value='empilhamento ativado', inline=False)
              elif quantidade in ['nao', 'n', 'false', 'falso']:
                del db['loja'][nome]['quantidade']
                embed.add_field(name=f"**quantidade**", value='empilhamento desativado', inline=False)
              else:
                embed.add_field(name=f"**quantidade**", value='opção não detectada!', inline=False)
            except Exception as error:
              embed.add_field(name=f"**quantidade**", value='erro na mudança de empilhamento', inline=False)
              print(error)
    except ValueError:
      embed=discord.Embed(title='valor usado não é um inteiro, use numeros, sem virgulas, sem pontos, sem letras e sem caracteres especieais.', color=0xdd0808)
    except Exception as error:
      embed=discord.Embed(title=f'erro na mudança de valores', color=0xdd0808)
      print(error)
  else:
    embed=discord.Embed(title='você não tem cargo suficiente.', color=0xdd0808)
  await envialog(message, 'ITEM MODIFICADO', f'item: {nome}\nmodificações:\n{f"novo nome é {novonome}. " if novonome != "none" else None}{f"novo preço é {preco}. " if preco != "none" else None}{f"novo cargo é {cargo}." if cargo != "none" else None}')
  await message.channel.send(embed=embed)

@bot.command()
async def delitem(message, nome): # para deletar um item
  global db
  if moderador in await cargos(message) or testeBot in await cargos(message) or dono == message.author.id:
    if not nome in db['loja'].keys():
      embed=discord.Embed(title="esse item não existe na loja.", color=0x3da560)
    else:
      del db['loja'][nome]
      embed=discord.Embed(title="item removido.", color=0x3da560)
      await envialog(message, 'ITEM DELETADO DA LOJA', f'o item {nome} foi deletado da loja por {message.author.mention}')
  else:
    embed=discord.Embed(title='você não tem cargo suficiente.', color=0xdd0808)
  await message.channel.send(embed=embed)

@bot.command()
async def addpp(message, quantia, mensao=None): # para adicionar um dinheiro
  global db
  if moderador in await cargos(message) or testeBot in await cargos(message) or dono == message.author.id:
    try:
      quantia = int(quantia)
      if mensao == None:
        if not str(message.author.id) in db.keys():
          await criacarteira(message)
        if quantia == 0:
          embed=discord.Embed(title="nada foi adicionado.", color=0x3da560)
        else:
          db[str(message.author.id)]['pp'] += quantia
          embed=discord.Embed(title=f'{quantia}pp adicionado na sua carteira', color=0x3da560)
          await envialog(message, 'DINHEIRO ADICIONADO', f'{quantia}pp adicionado para {message.author.mention} por ele mesmo')
      else:
        logmensao = mensao
        idmensao = await pegaid(mensao)
        mensao = message.guild.get_member(int(idmensao)).name
        if not str(idmensao) in db.keys():
          embed=discord.Embed(title=f'usuario {mensao} não encontrado.', color=0x3da560)
        elif quantia == 0:
          embed=discord.Embed(title=f'nada foi adicionado.', color=0x3da560)
        else:
          db[str(idmensao)]['pp'] += quantia
          embed=discord.Embed(title=f'{quantia}pp adicionado a carteira de {mensao}.', color=0x3da560)
          await envialog(message, 'DINHEIRO ADICIOADO', f'{quantia}pp adicionado a carteira de {logmensao} por {message.author.mention}')
    except ValueError:
      embed=discord.Embed(title='valor usado não é um inteiro, use numeros, sem virgulas, sem pontos, sem letras e sem caracteres especieais.', color=0xdd0808)
  else:
    embed=discord.Embed(title='você não tem cargo suficiente.', color=0xdd0808)
  await message.channel.send(embed=embed)

@bot.command()
async def delpp(message, quantia, mensao=None): # para tirar dinheiro
  global db
  if moderador in await cargos(message) or testeBot in await cargos(message) or dono == message.author.id:
    try:
      quantia = int(quantia)
      if mensao == None:
        if not str(message.author.id) in db.keys():
          await criacarteira(message)
        if quantia == 0:
          embed=discord.Embed(title=f'nada foi retirado.', color=0x3da560)
        else:
          if db[str(message.author.id)]['pp'] >= quantia:
            db[str(message.author.id)]['pp'] -= quantia
            embed=discord.Embed(title=f'{quantia}pp retirado da sua carteira.', color=0x3da560)
            await envialog(message, 'DINHEIRO RETIRADO', f'{quantia}pp foi retirado da carteira de {message.author.mention} por ele mesmo')
          else:
            embed=discord.Embed(title=f'pp não retirado, quantidade alta de mais, você não pode ficar com pp negativo.', color=0x3da560)
      else:
        logmensao = mensao
        idmensao = await pegaid(mensao)
        mensao = message.guild.get_member(int(idmensao)).name
        if not str(idmensao) in db.keys():
          embed=discord.Embed(title=f'usuario {mensao} não encontrado.', color=0x3da560)
        elif quantia == 0:
          embed=discord.Embed(title=f'nada foi removido.', color=0x3da560)
        else:
          if db[str(idmensao)]['pp'] >= quantia:
            db[str(idmensao)]['pp'] -= quantia
            embed=discord.Embed(title=f'{quantia}pp removido da carteira de {mensao}.', color=0x3da560)
            await envialog(message, 'DINHEIRO RETIRADO', f'{quantia}pp removido de {logmensao} por {message.author.mention}')
          else:
            embed=discord.Embed(title=f'quantia alta demais para ser removida, o usuario {mensao} não pode ficar com pp negativo.', color=0x3da560)
    except ValueError:
      embed=discord.Embed(title='valor usado não é um inteiro, use numeros, sem virgulas, sem pontos, sem letras e sem caracteres especieais.', color=0xdd0808)
  else:
    embed=discord.Embed(title='você não tem cargo suficiente.', color=0xdd0808)
  await message.channel.send(embed=embed)

@bot.command()
async def resetpp(message, mensao=None): # para resetar o dinheiro de alguem
  global db
  if moderador in await cargos(message) or testeBot in await cargos(message) or dono == message.author.id:
    if mensao == None:
      if not str(message.author.id) in db.keys():
        await criacarteira(message)
        embed=discord.Embed(title=f'seu dinheiro foi resetado.', color=0x3da560)
        await envialog(message, 'DINHEIRO RESETADO', f'o dinheiro de {message.author.mention} foi resetado por ele mesmo')
      else:
        db[str(message.author.id)]['pp'] = 0
        embed=discord.Embed(title=f'seu dinheiro foi resetado.', color=0x3da560)
        await envialog(message, 'DINHEIRO RESETADO', f'o dinheiro de {message.author.mention} foi resetado por ele mesmo')
    else:
      idmensao = await pegaid(mensao)
      if not idmensao in db.keys():
        embed=discord.Embed(title=f'{mensao} não possue uma carteira, {mensao} use !pp carteira para criar uma.', color=0xdd0808)
      else:
        db[idmensao]['pp'] = 0
        embed=discord.Embed(title=f'o dinheiro de {mensao} foi resetado.', color=0x3da560)
        await envialog(message, 'DINHEIRO RESETADO', f'o dinheiro de {mensao} foi resetado por {message.author.mention}')
  else:
    embed=discord.Embed(title='você não tem cargo suficiente.', color=0xdd0808)
  await message.channel.send(embed=embed)

@bot.command()
async def auditpp(message, novolog=None): # para mudar onde fica o log do bot
  global db
  if testeBot in await cargos(message) or moderador in await cargos(message) or dono == message.author.id:
    if novolog == None:
      try:
        embed=discord.Embed(title=f'grupo usado para log é: {message.guild.get_channel(logBot).name}.', color=0x3da560)
      except:
        embed=discord.Embed(title=f'chat não encontrado, use !pp auditpp #chat para mudar.', color=0x3da560)
    else:
      db['log'] = int(f'{novolog[2:-1]}')
      embed=discord.Embed(title=f'log redefinido.', color=0x3da560)
      await message.guild.get_channel(db['log']).send('log redefinido!.')
  else:
    embed=discord.Embed(title='você não tem cargo suficiente.', color=0xdd0808)
  await message.channel.send(embed=embed)

@bot.command()
async def comandpp(message, novochat): # para mudar onde serão executados os comandos
  if testeBot in await cargos(message) or moderador in await cargos(message) or dono == message.author.id:
    comandos = db['comandos']
    novocomandos = int(f'{novochat[2:-1]}')
    if comandos == novocomandos:
      embed=discord.Embed(title=f'os comandos ja estão sendo escutados nesse chat.', color=0x3da560)
      await message.channel.send(embed=embed)
    else:
      db['comandos'] = novocomandos
      embed=discord.Embed(title=f'chat de comando mudado para {message.guild.get_channel(novocomandos).name}.', color=0x3da560)
      await message.channel.send(embed=embed)
      embed=discord.Embed(title=f'chat de comando atualizado.', color=0x3da560)
      await message.guild.get_channel(novocomandos).send(embed=embed)
  else:
    embed=discord.Embed(title='você não tem cargo suficiente.', color=0xdd0808)
    await message.channel.send(embed=embed)

@bot.command()
async def daritem(message, nomeitem, mensao): # para dar um item seu a outro membro
  global db
  if testeBot in await cargos(message) or moderador in await cargos(message) or dono == message.author.id:
    if not str(message.author.id) in db.keys():
      await criacarteira(message)
    if nomeitem in db[str(message.author.id)]['itens'].keys():
      idMensao = await pegaid(mensao)
      if idMensao not in db.keys():
        embed.add_field(name="**usuario inesistente**", value=f'{mensao}!, use !pp carteira para criar sua carteira', inline=False)
      else:
        if nomeitem in db[str(await pegaid(mensao))]['itens'].keys():
          if 'quantidade' in db[str(await pegaid(mensao))]['itens'][nomeitem].keys():
            db[str(await pegaid(mensao))]['itens'][nomeitem]['quantidade'] += 1
            if db[str(message.author.id)]['itens'][nomeitem]['quantidade'] == 1:
              del db[str(message.author.id)]['itens'][nomeitem]
            else:
              db[str(message.author.id)]['itens'][nomeitem]['quantidade'] -= 1
            embed=discord.Embed(title=f'item enviado para {mensao}.', color=0x3da560)
            await envialog(message, 'ITEM TRANSFERIDO', f'{message.author.mention} enviou o item {nomeitem} para {mensao}')
          else:
            embed=discord.Embed(title=f'{mensao} já tem um item com esse nome e o item não é empilhavel.', color=0x3da560)
        elif db[str(message.author.id)]['itens'][nomeitem]['cargo'] in message.guild.get_member(int(await pegaid(mensao))).roles:
          if 'quantidade' in db[str(await pegaid(mensao))]['itens'][nomeitem].keys():
            db[str(await pegaid(mensao))]['itens'][nomeitem] = db[str(message.author.id)]['itens'][nomeitem].copy()
            if db[str(message.author.id)]['itens'][nomeitem]['quantidade'] == 1:
              del db[str(message.author.id)]['itens'][nomeitem]
            else:
              db[str(message.author.id)]['itens'][nomeitem]['quantidade'] -= 1
            db[str(await pegaid(mensao))]['itens'][nomeitem]['quantidade'] = 1
            embed=discord.Embed(title=f'item enviado para {mensao}.', color=0x3da560)
            await envialog(message, 'ITEM TRANSFERIDO', f'{message.author.mention} enviou o item {nomeitem} para {mensao}')
          else:
            embed=discord.Embed(title=f'{mensao} já tem um item com o cargo desse item e o item não é empilhavel.', color=0x3da560)
        else:
          if 'quantidade' in db[str(message.author.id)]['itens'][nomeitem].keys():
            db[str(await pegaid(mensao))]['itens'][nomeitem] = db[str(message.author.id)]['itens'][nomeitem].copy()
            db[str(await pegaid(mensao))]['itens'][nomeitem]['quantidade'] = 1
            if db[str(message.author.id)]['itens'][nomeitem]['quantidade'] == 1:
              del db[str(message.author.id)]['itens'][nomeitem]
            else:
              db[str(message.author.id)]['itens'][nomeitem]['quantidade'] -= 1
            embed=discord.Embed(title=f'item enviado para {mensao}.', color=0x3da560)
            await envialog(message, 'ITEM TRANSFERIDO', f'{message.author.mention} enviou o item {nomeitem} para {mensao}')
          else:
            db[str(await pegaid(mensao))]['itens'][nomeitem] = db[str(message.author.id)]['itens'][nomeitem].copy()
            del db[str(message.author.id)]['itens'][nomeitem]
            embed=discord.Embed(title=f'item enviado para {mensao}.', color=0x3da560)
            await envialog(message, 'ITEM TRANSFERIDO', f'{message.author.mention} enviou o item {nomeitem} para {mensao}')
    else:
      embed=discord.Embed(title='item não encontrado.', color=0xdd0808)
  else:
    embed=discord.Embed(title='você não tem cargo suficiente.', color=0xdd0808)
  await message.channel.send(embed=embed)

# comandos dono ---------------------------------------------------------------

@bot.command(name='resetallwalletsforeveyone')
async def resetEconomy(message): # para resetar toda a economia
  global db
  if testeBot in await cargos(message) or dono == message.author.id:
    global liberarResetEconomy
    global liberado
    if liberarResetEconomy == False:
      embed=discord.Embed(title=f'use o comando !pp confirm para confirmar\nuse o comando !pp resetallwalletsforeveyone em seguida para efetuar a exclusão.', color=0x000000)
      liberado = True
    else:
      for chave in db.keys():
        if chave == 'loja' or chave == 'log' or chave == 'comandos':
          continue
        else:
          del db[chave]
          resetEconomy(message)
          break
      for membro in message.guild.members:
        if not membro.bot:
          db[str(membro.id)] = {'pp':0,'itens':{}}
      embed=discord.Embed(title=f'{len(db.keys())} carteiras recriadas.', color=0x000000)
      liberarResetEconomy = False
      liberado = False
  else:
    embed=discord.Embed(title='você não tem cargo suficiente.', color=0xdd0808)
  await message.channel.send(embed=embed)

@bot.command()
async def confirm(message): # para confirmar o comando
  if testeBot in await cargos(message) or dono == message.author.id:
    global liberarResetEconomy
    global liberado
    if liberarResetEconomy == True:
      embed=discord.Embed(title=f'o comando !pp resetallwalletsforeveyone já foi liberado.', color=0x000000)
    else:
      if liberado == False:
        embed=discord.Embed(title=f'use o comando !pp resetallwalletsforeveyone para liberar esse comando.', color=0x000000)
      else:
        liberarResetEconomy = True
        embed=discord.Embed(title=f'o comando !pp resetallwalletsforeveyone foi liberado.', color=0x000000)
  else:
    embed=discord.Embed(title='você não tem cargo suficiente.', color=0xdd0808)
  await message.channel.send(embed=embed)

bot.run(config('TOKEN'))