# variaveis faltando <token do bot, chat do grupo, chat de erros>

from time import sleep as sl, time
from os import system as sys
try: # importação dos pacotes
    from playwright.sync_api import sync_playwright
    from requests import get
except Exception: # instalação dos pacotes não instalados
    print('instalando os pacotes: requests e playwrite')
    sl(3)
    sys('pip install requests')
    sys('pip install playwright')
    sys('playwright install')
    sys('cls')
    input('Por favor, feche e reinicie o programa.')
    exit()

CONFIGURACAO_DE_TESTE = False # coloque True para mandar mensagens das listas ao vivo

class TelegramBot(object):
    def __init__(self):

        self.TOKEN = 'token do bot' # token do bot criado pelo botfather (não tire as aspas)

        self.CHAT_ID = 'chat do grupo' # chat do grupo em que o bot vai ficar (não tire as aspas)
        self.CHAT_ID_ERRO = 'chat de erros' # chat do seu pv, para mensagens de erro (não tire as aspas)

        self.tentativas = 5

    def enviaMensagem(self, mensagem):
        while self.tentativas > 0:
            try:
                get(f'https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={self.CHAT_ID}&text={mensagem}')
                break
            except:
                sl(2)
                pass
        else:
            print('\no programa não esta conseguindo se conectar com o telegram, o bot foi desligado.\ntalvez você esteja sem internet ou passando por complicações, por favor, tente novamente mais tarde.')
            input()
            exit()

    def enviaMensagemDeErro(self, mensagem):
        while self.tentativas > 0:
            try:
                get(f'https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={self.CHAT_ID_ERRO}&text={mensagem}')
                break
            except:
                sl(2)
                pass
        else:
            print('\no programa não esta conseguindo se conectar com o telegram, o bot foi desligado.\ntalvez você esteja sem internet ou passando por complicações, por favor, tente novamente mais tarde.')
            input()
            exit()

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
        self.telegrambot = TelegramBot()

    def iniSite(self):

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.navegador = self.browser.new_page()
        self.navegador.goto(self.SITE)

        sys('cls')
        sys('@title Bot Double')
        print('Bot iniciado.')

    def pegaCor(self):
        while True:
            carregamento = self.navegador.locator('//*[@id="roulette-timer"]/div[1]').text_content()
            try:
                if carregamento.split()[0] == 'Blaze':
                    num = carregamento.split()[2][0:-1]
                    if int(num) == 0:
                        return 'branco'
                    elif int(num) <= 7:
                        return 'vermelho'
                    else:
                        return 'preto'
            except:
                pass

    def finais(self, cor):

        sec0 = self.sec0
        sec1 = self.sec1
        sec2 = self.sec2
        sec3 = self.sec3
        sec4 = self.sec4

        if len(self.sec0) == 4 and self.sec0[0] != cor or len(self.sec1) == 9 and self.sec1[8] == cor or len(self.sec2) == 5 and self.sec2[4] == cor or len(self.sec3) == 4 and self.sec3[3] == cor or len(self.sec4) == 6 and self.sec4[4] == cor:
            self.telegrambot.enviaMensagem('Abortar missão ❗️') # previsão errada

        if len(self.sec0) > 4 and self.sec0[0] != cor or len(self.sec1) > 9 and self.sec1[9] != cor or len(self.sec2) > 5 and self.sec2[5] != cor or len(self.sec3) > 4 and self.sec3[4] != cor or len(self.sec4) > 6 and self.sec4[5] != cor:
            self.telegrambot.enviaMensagem('Green ✅ 🤑') # previsão certa
            self.green[f'green{len(self.green)}'] = int(time()) 
            for i in range(4+1):
                exec(f'sec{i}.clear()')

        elif len(self.sec0) > 4 and cor == 'branco' or len(self.sec1) > 9 and cor == 'branco' or len(self.sec2) > 5 and cor == 'branco' or len(self.sec3) > 4 and cor == 'branco' or len(self.sec4) > 6 and cor == 'branco':
            self.telegrambot.enviaMensagem('Green ✅ 🤑') # previsão certa sendo branco
            self.green[f'green{len(self.green)}'] = int(time())
            for i in range(4+1):
                exec(f'sec{i}.clear()')

    def esperar(self):
        while True:
            carregamento = self.navegador.locator('//*[@id="roulette-timer"]/div[1]').text_content()
            try:
                if carregamento.split()[0] == 'Girando' or carregamento.text.split()[0] == 'Girando...':
                    return
            except:
                pass

    def jogadas(self, cor):

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
                if gale <= 2:
                    self.telegrambot.enviaMensagem(f'Aviso vamos ao {gale}º gale 🍀')
                if gale == 3:
                    self.telegrambot.enviaMensagem('Não foi dessa vez, mas mantenha a calma!')
                    self.loss[f'loss{len(self.loss)}'] = int(time())
                    sec.clear()

        def foca(sec, n):
            n = n-1
            sec0 = self.sec0
            sec1 = self.sec1
            sec2 = self.sec2
            sec3 = self.sec3
            sec4 = self.sec4
            for i in range(4+1):
                exec(f'if len({sec}) > {n}:\n\tif {sec} == sec{i}:\n\t\tpass\n\telse:\n\t\tsec{i}.clear()')
                # função encurtada usando exec, ela limpa as outras sequencias caso uma esteja em foco
                # em foco é quando ela entrou no padrão, para n dar conflito ela é limpada

        foca('sec0', 4)
        if len(self.sec0) == 0:
            self.sec0.append(cor)
        else:
            if len(self.sec0) <= 4:
                igual(self.sec0, 0)
            else:
                addgale(self.sec0, 7, 3)
                addgale(self.sec0, 6, 2)
                addgale(self.sec0, 5, 1)

        foca('sec1', 9)
        if len(self.sec1) == 0:
            self.sec1.append(cor)
        else:
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
            addgale(self.sec3, 7, 3)
            addgale(self.sec3, 6, 2)
            addgale(self.sec3, 5, 1)
            # gale ^
            diferente(self.sec3, 3, 4)
            diferente(self.sec3, 2, 3)
            diferente(self.sec3, 1, 2)
            diferente(self.sec3, 0, 1)
            
        foca('sec4', 6) 
        if len(self.sec4) == 0:
            self.sec4.append(cor)
        else:
            addgale(self.sec4, 8, 3)
            addgale(self.sec4, 7, 2)
            addgale(self.sec4, 6, 1)
            # gale ^
            diferente(self.sec4, 5, 6)
            diferente(self.sec4, 4, 5)
            diferente(self.sec4, 3, 4)
            diferente(self.sec4, 2, 3)
            igual(self.sec4, 1, 2)
            diferente(self.sec4, 0, 1)

    def aviso(self, cor):

        if len(self.sec0) == 4 or len(self.sec1) == 9 or len(self.sec2) == 5 or len(self.sec3) == 4 or len(self.sec4) == 5:
            self.telegrambot.enviaMensagem(f'Aviso! possivel entrada, favor aguardar.\nhttps://blaze.com/pt/games/double')

        if len(self.sec0) == 5 or len(self.sec1) == 10 or len(self.sec2) == 6 or len(self.sec3) == 5 or len(self.sec4) == 6:
            self.telegrambot.enviaMensagem(f'Aviso! entrada confirmada na cor {"🟥" if cor == "preto" else "⬛️"} ({"vermelho" if cor == "preto" else "preto"})')
            self.confirm_cor = 'vermelho' if cor == 'preto' else 'preto'

        self.esperar()

class Program(object):
    def __init__(self):

        self.site = Site()
        self.telegrambot = TelegramBot()

        try:
            self.site.iniSite()
        except Exception:
            sys('cls')
            print('ops, ocorreu um erro ao iniciar o site para você, o bot foi desligado.\ntalvez você esteja sem internet ou passando por complicações, tente novamente mais tarde.')
            input()
            exit()

        try:
            while True:
                cor = self.site.pegaCor()
                self.site.finais(cor)
                self.site.jogadas(cor)
                self.site.aviso(cor)

                if CONFIGURACAO_DE_TESTE == True: # log ao vivo
                    self.telegrambot.enviaMensagemDeErro(f'{cor}\n{self.site.sec0}\n{self.site.sec1}\n{self.site.sec2}\n{self.site.sec3}\n{self.site.sec4}\n.') # configuração de teste

                self.optmizacaoGreenLoss()
            
        except KeyboardInterrupt: # se caso o programa for interrompido pelo usuario
            print('\ninterrompendo o programa e iniciando o fechamento do dia...')

            if len(self.site.green) != 0 or len(self.site.loss) != 0:
                self.telegrambot.enviaMensagem(f'Fechamento do dia:\n{len(self.site.green)} green{"s" if len(self.site.green) > 1 else ""} e {len(self.site.loss)} loss.')
                print('fechamento enviado, ', end='')
            else:
                print('fechamento do dia zerado, ', end='')

            print('finalizando programa.')
            sl(5)
            exit()

        except: # se caso der algum erro inesperado
            print('ops, algo deu errado...\nvamos tentar reiniciar o programa pra ver se resolve')

            if len(self.site.green) != 0 or len(self.site.loss) != 0:
                self.telegrambot.enviaMensagem(f'Fechamento do dia:\n{len(self.site.green)} green{"s" if len(self.site.green) > 1 else ""} e {len(self.site.loss)} loss.')

            self.telegrambot.enviaMensagemDeErro(f'algo deu errado com o bot, mas já estamos reiniciando pra ver se resolve')

            sl(5)
            sys('python main.py')
            exit()

    def optmizacaoGreenLoss(self): # como o programa salva os green e loss, essa otimização é apenas para limpar os green e loss salvos a mais de 24 horas
        tempo = time()

        for chave, valor in self.site.green.items():
            if tempo - valor <= 86400 and tempo - valor >= 0:
                continue
            else:
                del self.site.green[chave]
                self.optmizacaoGreenLoss()
                break
                    
        for chave, valor in self.site.loss.items():
            if tempo - valor <= 86400 and tempo - valor >= 0:
                continue
            else: 
                del self.site.loss[chave]
                self.optmizacaoGreenLoss()
                break

Program()
