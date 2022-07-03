<p align='center'><img src='https://user-images.githubusercontent.com/59841892/166121885-e9a3a39f-f389-4cea-8116-445ef27d1333.png' height="300" width="300"></p>
<h1 align='center'>Invited</h1>

Segundo projeto

O bot, conectado em um servidor do discord, simula um sistema de compra e venda de cargos, podendo adiconar e remover dinheiro virtual, adicionar e remover itens a venda etc...

Os itens comprados podem ser substituidos por dinheiro real e por outros cargos:

![imagem mostrando comandos e respostas do bot](https://user-images.githubusercontent.com/59841892/166121716-499e5512-ed06-49db-a577-9b1fc9d81dcb.PNG)

O bot pode ser moderado pelo próprio servidor, tendo até um sistema de log:

![imagem do chat de log do bot](https://user-images.githubusercontent.com/59841892/166121725-d1a2ab2b-6844-4395-ba0d-c535356430a8.PNG)

# BANCO DE DADOS EM GIT

o primeiro problema que encontrei foi a persistencia em banco de dados, depois de umas 3 horas, o banco de dados era formatado, então tive a ideia de manter o banco de dados em git, quando o bot iniciar, irá pegar o banco de dados no github, quando quiser escrever, é só atualizar o repositório, assim eu fiz, com esse trecho:

```py
def pegadb():
  return eval(git.get_user().get_repo(mainrepo).get_contents('/')[indice].decoded_content.decode('utf-8'))

async def escrevedb(db):
  repo = git.get_user().get_repo(mainrepo)
  contents = repo.get_contents('/')[indice]
  repo.update_file(contents.path, "", str(db), contents.sha)
```

# tentei usar, mas não consegui, o que faço?

tem muitas variaveis faltando, quando abrir o codigo, vera, no lugar da variaveis, textos, falando o que vai lá, ex:
```py
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
```
tokens, ids, e indices devem ser inteiros, nomes devem estar entre aspas

# tentei executar, mas ele desliga sozinho, o que faço?

o bot tem que estar em um servidor, e tambêm, você tem que ter um repositório no git (de preferencia, privado), com esse esquema:
![imagem do esquema de pastas](https://user-images.githubusercontent.com/59841892/166122295-a16aa222-6e60-4531-9510-d2a76e464873.PNG)
<br>o arquivo db.txt deve ter esse codigo:
`{'log': None, 'loja': {}, 'comandos': None}`
#
tambem é necessario instalar o python na sua maquina, você pode fazer a instalação [aqui](https://www.python.org/ftp/python/3.10.4/python-3.10.4-amd64.exe)
logo após a instalação é só usar o comando 
<br>`python main.py`
#
depois de instalar o python pode não funcionar, você precissa instalar as dependencias, use ocomando `pip install -r requirements.txt` na pasta do projeto
#
se caso não funcionar, você pode ter esquecido de criar um bot, recomendo pesquisar no google como criar um bot, você irá precisar do token dele, na ultima linha do codigo, tem o token faltando:
`bot.run(config('TOKEN'))`
# 

<p align='center'>qualquer coisa só chamar</p>
<p align='center'>meu discord / whatsapp:</p>
<p align='center'>Purple-Senpai#7642 / (47) 992423806</p>
