import requests

class telegramBot:

    def __init__(self, token):
        self.token = token
        self.url = f'https://api.telegram.org/bot{token}'
        self.offset = 0
        self.send_message_url = f'{self.url}/sendMessage'
        self.get_updates_url = f'{self.url}/getUpdates'

    def getUpdates(self):
        params = {'offset': self.offset, 'allowed_updates': ['message']}
        response = requests.get(self.get_updates_url, params)
        data = response.json()
        if data['ok'] and len(data['result']) != 0:
            self.offset=(data['result'][-1]['update_id']) + 1
        return data['result']

    def sendMessage(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        response = requests.post(self.send_message_url, params)
        return response.json()

    def setUpNewUser(self, chat_id):
        self.sendMessage(chat_id, 'Benvenuto in BotBenzinaio!')
        # self.sendMessage(chat_id, 'Ho bisogno di un paio di funzioni per poterti aiutare')
        # self.sendMessage(chat_id, 'Per prima cosa, quanto e` capiente il tuo serbatoio (in litri)?')
        # self.sendMessage(chat_id, 'Quanto consuma la tua auto (in l/100km)?')
        # self.sendMessage(chat_id, 'Che tipo di carburante usi?')
        # self.sendMessage(chat_id, 'Quanti kilometri sei diposto a percorrere per fare benzina?')
        # self.sendMessage(chat_id, 'Ottimo! Ora sei pronto per iniziare ad usare il bot!')
        self.sendMessage(chat_id, 'Per iniziare, digita /help')

    def sendHelp(self, chat_id):
        self.sendMessage(chat_id, 
    '''
    Ecco la lista dei comandi disponibili

/carburante - imposta il tipo di carburante
/consumo - imposta il consumo (in l/100km)
/serbatoio - imposta la capienza del serbatoio
/km - imposta il numero di kilometri che sei disposto a percorrere per fare benzina
/help - mostra la lista dei comandi disponibili
''')
