<p align="center"><img src="https://user-images.githubusercontent.com/59841892/166119077-2d9d3201-5922-415f-8490-bcece3db3364.png" height="300" width="300"></p>
<h1 align="center"> Double Kings </h1>
<p>
O bot, no site da Blaze, no jogo Double (você pode dar uma olhada <a href="https://blaze.com/pt/games/double">aqui</a>), retira as jogadas de cada partida e com os padrões salvos, tenta descobrir qual sera a proxima jogada.
As respostas do bot são feitas pelo telegram.
</p>
<img src="https://user-images.githubusercontent.com/59841892/166119477-243de44d-2324-4f8b-ad4e-4654e4d85f73.PNG">
<p>Aqui mostra o bot avisando de uma possivel entrada, depois confirmando a entrada da cor vermelha, e logo em seguida mostra susseso na previsão.</p>
<p>nesse projeto usei selenium para retirar dados do site, usei a rest api do telegram para mandar as mensagens e hospedei o bot em dois servidores, o google clound e aws.</p>
<p>como o site bloqueia ip de varios paises, opções gratuitas foram mais dificeis de achar.</p>
<h1 align="center">quero usar, como fazer?</h1>
<p>primeiro você deve baixar o codigo</p>
<p>Depois, deve abri-lo em uma IDE ou em um editor de texto qualquer pois tem variaveis faltando nele, por segurança, as variaveis onde devem conter um id de um grupo do telegram, id privado para erros e um token de um bot devem ser preenchidos</p>
<p>linha 23, 25 e 26:</p>
<img src="https://user-images.githubusercontent.com/59841892/176346182-01792bef-642d-4bcd-8fbf-e8111a3579bb.png">
<p>É bem pouco provavel haver erros, mas qualquer erro que ocorrer será automaticamente enviado para você, e o programa ira reiniciar automaticamente</p>
<h1></h1>
<ul>
<li>criando um bot
<p>É necessario criar um bot no telegram, para enviar as mensagens pra você:</p>
<ol type="1">
<li>Crie uma conta no Telegram
<li>Inicie uma conversa com o @botfather (lembre-se que os robôs oficiais do Telegram têm um tique azul do lado do nome)
<li>Clique em iniciar
<li>Escolha o comando /newbot
<li>Escolha o nome do seu chatbot e faça as configurações gerais
<li>Copie o token, e cole no codigo, na linha <code>27: self.TOKEN = 'token do bot'</code> <- aqui onde ta escrito token do bot !(mantenha as aspas)!
</ol>
<p>!lembrando que o bot deve estar dentro do grupo e como adm, para poder mandar as mensagens!</p>
<h1></h1>
<li>pegando o id de um grupo
<p>
Recomendo este <a href="https://blog.gabrf.com/posts/TelegramID/#:~:text=Caso%20queira%20o%20ID%20de,basta%20verificar%20em%20from%20id%20.">link</a>, ele levara você até com instruções para pegar o id do grupo, pois as instruções são muito longas
</p>
<h1></h1>
<li>instalando python
<p>Nesse <a href="https://www.python.org/ftp/python/3.10.4/python-3.10.4-amd64.exe">link</a> você pode baixar o python, é só seguir as instruções de download.</p>
<h1></h1>
<li>instalando dependencias
<p>
se caso você não instalou as dependencias antes de executar o programa, ele irá instalar automaticamente e pedira pra você reiniciar-lo, para assim funcionar normalmente, mas se caso isso não acontecer:<br>
Abra o cmd dentro da pasta do projeto, e use o comando:
<code>pip install -r requirements.txt</code>
</p>
<p>todos os programas necesarios para o funcionamento do bot serão instalado</p>
<h1></h1>
<li>executando o bot
<p>se caso você clicou duas vezes no programa e ele não abriu, então:</p>
<p>ainda com o cmd aberto, basta digitar <code>python main.py</code>, e o programa será iniciado</p>
<p>ele funcionara na sua maquina, para funcionar em nuvem, basta colocalo em um servidor e colocar o comando de execução <code>python main.py</code> no console</p>
<h1></h1>
<li>sobre o código
<p>
não me orgulho muito dele, agora que tenho mais experiência, entendo que poderia fazer de forma mais simples, em algumas partes ele é bem confuso, eu poderia ter usado apenas uma variavel para armazenar as cores, e um codigo pequeno para cada sequencia poder analizar a variavel des cores, com uma variavel booleana para controlar-las, seria bem mais facil, porem ele funciona, e faz o que deve ser feito.
</p>
<h1></h1>
<br>
<p align='center'>qualquer coisa só chamar</p>
<p align='center'>meu discord / whatsapp:</p>
<p align='center'>Purple-Senpai#7642 / (47) 992423806</p>
