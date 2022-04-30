<p align="center"><img src="https://user-images.githubusercontent.com/59841892/166119077-2d9d3201-5922-415f-8490-bcece3db3364.png" height="300" width="300"></p>
<h1 align="center"> bot blaze telegram </h1>

meu primeiro projeto


O bot, no site da Blaze, no jogo Double (você pode dar uma olhada [aqui](https://blaze.com/pt/games/double)), retira as jogadas de cada partida e com os padrões salvos, tenta descobrir qual sera a proxima jogada.
As respostas do bot são feitas pelo telegram.

A margem de erro do bot é menor que 5%, pois usa um sistema de multiplicação da aposta quando o padrão é esticado.

![imagem das respostas do bot](https://user-images.githubusercontent.com/59841892/166119477-243de44d-2324-4f8b-ad4e-4654e4d85f73.PNG)

Aqui mostra o bot avisando de uma possivel entrada, depois confirmando a entrada da cor vermelha, e logo em seguida mostra susseso na previsão.

<h1 align="center">quero usar, como fazer?</h1>
primeiro você deve baixar o codigo

Depois, deve abri-lo em uma IDE ou em um editor de texto qualquer pois tem variaveis faltando nele, por segurança, as variaveis onde devem conter um id de um grupo do telegram, id privado para erros e um token de um bot devem ser preenchidos

É bem pouco provavel haver erros, mas qualquer erro que ocorrer será automaticamente enviado para você, e o programa ira reiniciar automaticamente

* criando um bot

É necessario criar um bot no telegram, para enviar as mensagens pra você:

1. Crie uma conta no Telegram
2. Inicie uma conversa com o @botfather (lembre-se que os robôs oficiais do Telegram têm um tique azul do lado do nome)
3. Clique em iniciar
4. Escolha o comando /newbot
5. Escolha o nome do seu chatbot e faça as configurações gerais
6. Copie o token, e cole no codigo, na linha 27: self.TOKEN = 'token do bot' <- aqui onde ta escrito token do bot !(mantenha as aspas)!

!lembrando que o bot deve estar dentro do grupo, para poder mandar as mensagens!

* pegando o id de um grupo

Recomendo este [link](https://blog.gabrf.com/posts/TelegramID/#:~:text=Caso%20queira%20o%20ID%20de,basta%20verificar%20em%20from%20id%20.), ele levara você até com instruções para pegar o id do grupo, pois as instruções são muito longas

* instalando python

Nesse [link](https://www.python.org/ftp/python/3.10.4/python-3.10.4-amd64.exe) você pode baixar o python, é só seguir as instruções de download.

* instalando dependencias

Abra o cmd dentro da pasta do projeto, e use o comando:
`pip install -r requirements.txt`

todos os programas necesarios para o funcionamento do bot serão instalado

* executando o bot

ainda com o cmd aberto, basta digitar `python main.py`, e o programa será iniciado

ele funcionara na sua maquina, para funcionar em nuvem, basta colocalo em um servidor e colocar o comando de execução `python main.py` no console

#

irei disponibilizar um link posteriormente para poder entrar em um servidor do telegram e ver o bot em ação!
