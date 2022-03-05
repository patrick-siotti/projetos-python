# programa feito para retirada de infromações do site blaze do jogo double, as informações são revisadas, na tentativa de encontrar uma possivel entrada

# programa sem informações de chat nem bot

# esse foi o primeiro projeto que fiz

try: # importação dos pacotes
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
    from requests import get
    from os import system as sys
    from time import sleep as sl, time
except Exception: # instalação dos pacotes não instalados
    print('instalando os pacotes: requests, webdriver-manager, selenium e keyboard')
    sys('pip install requests')
    sys('pip install webdriver-manager')
    sys('pip install selenium')
    sys('pip install keyboard')
    sys('cls')
    print('reiniciando o programa...')
    sys('python main.py')
    exit()

class TelegramBot(object):
    def __init__(self):
        self.TOKEN = 'token do bot'

        self.CHAT_ID = 'chat do grupo'
        self.CHAT_ID_ERRO = 'chat de erros'

        self.enviaMensagem = lambda mesage: get(f'https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={self.CHAT_ID}&text={mesage}')
        self.enviaMensagemDeErro = lambda mesage: get(f'https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={self.CHAT_ID_ERRO}&text={mesage}')

class Site(object):
    def __init__(self):
        self.sec0 = [] # sec0 == sequencia0
        self.sec1 = []
        self.sec2 = []
        self.sec3 = []
        self.sec4 = []
        self.green = {} # acertos
        self.loss = {} # erros
        self.confirm_cor = ''
        self.SITE = 'https://blaze.com/pt/games/double'

    def iniSite(self):
        # telegrambot = TelegramBot()

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')

        self.navegador = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options) # instala os drivers automaticamente, e o site é aberto de forma "--headless", ou seja, escondido
        self.navegador.get(self.SITE)

        sys('cls')
        sys('@title Bot Double')
        print('Bot iniciado.')
        print('mensagem para grupo free desativado.')
        # telegrambot.enviaMensagem('Bot iniciado')

    def pegaCor(self):
        while True:
            carregamento = self.navegador.find_element(By.XPATH, '//*[@id="roulette-timer"]/div[1]')
            
            try:
                if carregamento.text.split()[0] == 'Blaze':
                    num = carregamento.text.split()[2][0:-1]
                    if int(num) == 0:
                        return 'branco'
                    elif int(num) <= 7:
                        return 'vermelho'
                    else:
                        return 'preto'
            except:
                pass

    def finais(self, cor):
        telegrambot = TelegramBot()

        # peço desculpa pelo if longo de mais akkak

        if len(self.sec0) == 4 and self.sec0[0] != self.confirm_cor or len(self.sec1) == 9 and self.sec1[8] == self.confirm_cor or len(self.sec2) == 5 and self.sec2[4] == self.confirm_cor or len(self.sec3) == 4 and self.sec3[3] == self.confirm_cor or len(self.sec4) == 5 and self.sec4[4] == self.confirm_cor:
            telegrambot.enviaMensagem('Abortar missão ❗️') # previsão errada

        if len(self.sec0) > 4 and self.sec0[0] != self.confirm_cor or len(self.sec1) > 9 and self.sec1[9] != self.confirm_cor or len(self.sec2) > 5 and self.sec2[5] != self.confirm_cor or len(self.sec3) > 4 and self.sec3[4] != self.confirm_cor or len(self.sec4) > 5 and self.sec4[5] != self.confirm_cor:
            telegrambot.enviaMensagem('Green ✅ 🤑') # previsão certa
            self.green[f'green{len(self.green)}'] = int(time()) 
            for i in range(4+1):
                exec(f'sec{i}.clear()')

        elif len(self.sec0) > 4 and cor == 'branco' or len(self.sec1) > 9 and cor == 'branco' or len(self.sec2) > 5 and cor == 'branco' or len(self.sec3) > 4 and cor == 'branco' or len(self.sec4) > 5 and cor == 'branco':
            telegrambot.enviaMensagem('Green ✅ 🤑') # previsão certa
            self.green[f'green{len(self.green)}'] = int(time())
            for i in range(4+1):
                exec(f'sec{i}.clear()')

    def esperar(self):
        while True:
            carregamento = self.navegador.find_element(By.XPATH, '//*[@id="roulette-timer"]/div[1]')
            try:
                if carregamento.text.split()[0] == 'Girando' or carregamento.text.split()[0] == 'Girando...':
                    return
            except:
                pass

    def jogadas(self, cor):
        telegrambot = TelegramBot()

        def diferente(sec, n, cont=''): # se caso a cor atual for diferente da cor antiga
            if n+1 <= len(sec) and cont == '':
                cor if sec[n] != cor else sec.clear()
                sec.append(cor)
            elif n+1 <= len(sec) and cont == len(sec):
                sec.append(cor) if sec[n] != cor else sec.clear()

        def igual(sec, n, cont=''):
            if n+1 <= len(sec) and cont == '':
                cor if sec[n] == cor else sec.clear()
                sec.append(cor)
            elif n+1 <= len(sec) and cont == len(sec):
                sec.append(cor) if sec[n] == cor else sec.clear()

        def addgale(sec, n, gale): # se caso a cor se repetir, ele repetira a previsão
            global loss

            if len(sec) == n:
                if sec[-1] == cor:
                    sec.append(cor)
            if len(sec) == n+1:
                if gale <= 3:
                    telegrambot.enviaMensagem(f'Aviso vamos ao {gale}º gale 🍀')
                if gale == 4:
                    telegrambot.enviaMensagem('Não foi dessa vez, mas mantenha a calma!')
                    self.loss[f'loss{len(self.loss)}'] = int(time())
                    sec.clear()

        def foca(sec, n):
            sec0 = self.sec0
            sec1 = self.sec1
            sec2 = self.sec2
            sec3 = self.sec3
            sec4 = self.sec4
            n = n-1
            for i in range(4+1):
                exec(f'if len({sec}) > {n}:\n    if {sec} == sec{i}:\n        pass\n    else:\n        sec{i}.clear()')
                # função encurtada usando exec, ela limpa as outras sequencias caso uma esteja em foco

        foca('sec0', 4)
        if len(self.sec0) == 0:
            self.sec0.append(cor)
        else:
            if len(self.sec0) <= 4:
                igual(self.sec0, 0)
            else:
                addgale(self.sec0, 8, 4)
                addgale(self.sec0, 7, 3)
                addgale(self.sec0, 6, 2)
                addgale(self.sec0, 5, 1)

        foca('sec1', 9)
        if len(self.sec1) == 0:
            self.sec1.append(cor)
        else:
            addgale(self.sec1, 13, 4)
            addgale(self.sec1, 12, 3)
            addgale(self.sec1, 11, 2)
            addgale(self.sec1, 10, 1)
            # gale ^
            diferente(self.sec1, 8, 9)
            igual(self.sec1, 7, 8)
            diferente(self.sec1, 6, 7)
            diferente(self.sec1, 5, 6)
            igual(self.sec1, 4, 5)
            diferente(self.sec1, 3, 4)
            diferente(self.sec1, 2, 3)
            igual(self.sec1, 1, 2)
            diferente(self.sec1, 0, 1)

        foca('sec2', 5)
        if len(self.sec2) == 0:
            self.sec2.append(cor)
        else:
            addgale(self.sec2, 9, 4)
            addgale(self.sec2, 8, 3)
            addgale(self.sec2, 7, 2)
            addgale(self.sec2, 6, 1)
            # gale ^
            diferente(self.sec2, 4, 5)
            diferente(self.sec2, 3, 4)
            diferente(self.sec2, 2, 3)
            igual(self.sec2, 1, 2)
            igual(self.sec2, 0, 1)
 
        foca('sec3', 4) 
        if len(self.sec3) == 0:
            self.sec3.append(cor)
        else:
            addgale(self.sec3, 8, 4)
            addgale(self.sec3, 7, 3)
            addgale(self.sec3, 6, 2)
            addgale(self.sec3, 5, 1)
            # gale ^
            diferente(self.sec3, 3, 4)
            diferente(self.sec3, 2, 3)
            diferente(self.sec3, 1, 2)
            diferente(self.sec3, 0, 1)
            
        foca('sec4', 5) 
        if len(self.sec4) == 0:
            self.sec4.append(cor)
        else:
            addgale(self.sec4, 9, 4)
            addgale(self.sec4, 8, 3)
            addgale(self.sec4, 7, 2)
            addgale(self.sec4, 6, 1)
            # gale ^
            diferente(self.sec4, 4, 5)
            diferente(self.sec4, 3, 4)
            diferente(self.sec4, 2, 3)
            igual(self.sec4, 1, 2)
            diferente(self.sec4, 0, 1)

    def aviso(self, cor):
        telegrambot = TelegramBot()

        if len(self.sec0) == 4 or len(self.sec1) == 9 or len(self.sec2) == 5 or len(self.sec3) == 4 or len(self.sec4) == 5:
            telegrambot.enviaMensagem(f'Aviso! possivel entrada, favor aguardar.\nhttps://blaze.com/pt/games/double')

        if len(self.sec0) == 5 or len(self.sec1) == 10 or len(self.sec2) == 6 or len(self.sec3) == 5 or len(self.sec4) == 6:
            telegrambot.enviaMensagem(f'Aviso! entrada confirmada na cor {"🟥" if cor == "preto" else "⬛️"}')
            self.confirm_cor = 'vermelho' if cor == 'preto' else 'preto'

        self.esperar()

class Program(object):
    def __init__(self):
        site = Site()
        telegrambot = TelegramBot()
        self.texteNet = lambda: sys('ping google.com') # testa conexão

        site.iniSite()

        try:
            while True:
                cor = site.pegaCor()
                site.finais(cor)
                site.jogadas(cor)
                site.aviso(cor)

                # telegrambot.enviaMensagem(site.sec0)
                # telegrambot.enviaMensagem(site.sec1)
                # telegrambot.enviaMensagem(site.sec2)
                # telegrambot.enviaMensagem(site.sec3)
                # telegrambot.enviaMensagem(site.sec4)
                # telegrambot.enviaMensagem('.') # configuração de teste

                self.optmizacaoGreenLoss()
            
        except KeyboardInterrupt:
            while self.texteNet() == 1:
                sl(5)    

            if len(site.green) != 0 or len(site.loss) != 0:
                telegrambot.enviaMensagem(f'Fechamento do dia:\n{len(site.green)} green{"s" if len(site.green) > 1 else ""} e {len(site.loss)} loss.')
            exit()

        except Exception as error:
            print(f'\nerro inesperado na execução do programa:\n{error}\n\ntentativa de reinicialização do programa...\n')
            while self.texteNet() == 1:
                sl(5)    

            if len(site.green) != 0 or len(site.loss) != 0:
                telegrambot.enviaMensagem(f'Fechamento do dia:\n{len(site.green)} green{"s" if len(site.green) > 1 else ""} e {len(site.loss)} loss.')

            telegrambot.enviaMensagemDeErro(f'erro no programa principal\nerro inesperado:\n{error}')
            sys('python main.py')
            exit()

    def optmizacaoGreenLoss(self): # como o programa salva os green e loss, essa otimização é apenas para limpar os green e loss salvos a mais de 24 horas
        site = Site()
        tempo = time()

        for chave, valor in site.green.items():
            if tempo - valor <= 86400 and tempo - valor >= 0:
                continue
            else:
                del site.green[chave]
                self.optmizacaoGreenLoss()
                break
                    
        for chave, valor in site.loss.items():
            if tempo - valor <= 86400 and tempo - valor >= 0:
                continue
            else: 
                del site.loss[chave]
                self.optmizacaoGreenLoss()
                break

Program()