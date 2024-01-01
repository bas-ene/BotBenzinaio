#imports
from time import sleep
from sqlConnector import sqlConnector
from telegramBot import telegramBot
import requests,json, threading
#global vars
path_bottoken = './data/token_bot.json'
url_bot_telegram = 'https://api.telegram.org/bot'

#functions
def readBotToken():
    bot_token = ''
    with open(path_bottoken, 'r') as bot_token_file:
        bot_token = json.loads(bot_token_file.read())['token']
    return bot_token

def downloadFile(url, outputFile):
    with requests.get(url) as r:
        outputFile.write(r.text)
        r.close()   
        return r.text

def parse_command(command):
    command = command.split(' ')
    if(len(command) < 2):
        return False
    else:
        return ' '.join(command[1:])


#main func
if __name__ == "__main__":
   
    #download updated prices and details about gas pumps
    # with open('./data/prezzi.csv', 'w') as file_prezzi:
    #     csv_data_prezzi = downloadFile('https://www.mimit.gov.it/images/exportCSV/prezzo_alle_8.csv', file_prezzi)
    # with open('./data/anagrafica.csv', 'w') as  file_anagrafica :
    #     csv_data_anag = downloadFile('https://www.mimit.gov.it/images/exportCSV/anagrafica_impianti_attivi.csv', file_anagrafica)
    #create sql connection
    conn = sqlConnector('./data/db_config.json')
    #put the csv info in the 

    #get bot 
    telBot = telegramBot(readBotToken())
    while True:
        #get new messages
        data = telBot.getUpdates()
        #check if there are new messages
        if(data == []):
            print('no new messages')
            continue

        #for each message
        for message in data:
            user_id = message['message']['from']['id']
            username = message['message']['from']['username']
            #get if is a new user
            if(conn.getUser(user_id) == []):
                print('new user')
                #insert new user
                conn.insertUser(user_id, username)
                telBot.setUpNewUser(user_id)
            else:
                print('old user')
            #get the type of message
            message_text = message['message']['text']
            if(message_text == '/help'):
                telBot.sendHelp(user_id)
            elif(message_text.startswith('/carburante')):
                #set carburante
                value = parse_command(message_text)
                if(value):
                    success = conn.setCarburante(user_id, value)
                    if(success):
                        telBot.sendMessage(user_id, 'Carburante impostato correttamente')
                    else:
                        telBot.sendMessage(user_id, 'Errore durante l\'impostazione del carburante, potrebbe non essere nel nostro database')
                else:
                    telBot.sendMessage(user_id, 'Devi specificare il tipo di carburante')
            elif(message_text.startswith('/consumo')):
                #set consumo
                value = parse_command(message_text)
                if(value):
                    success = conn.setConsumo(user_id, value)
                    if(success):
                        telBot.sendMessage(user_id, 'Consumo impostato correttamente')
                    else:
                        telBot.sendMessage(user_id, 'Errore durante l\'impostazione del consumo')
                else:
                    telBot.sendMessage(user_id, 'Devi specificare il consumo')
            elif(message_text.startswith('/serbatoio')):
                #set serbatoio
                value = parse_command(message_text)
                if(value):
                    success = conn.setSerbatoio(user_id, value)
                    if(success):
                        telBot.sendMessage(user_id, 'Serbatoio impostato correttamente')
                    else:
                        telBot.sendMessage(user_id, 'Errore durante l\'impostazione del serbatoio')
                else:
                    telBot.sendMessage(user_id, 'Devi specificare la capienza del serbatoio')
            elif(message_text.startswith('/km')):
                #set km
                value = parse_command(message_text)
                if(value):
                    success = conn.setMaxKm(user_id, value)
                    if(success):
                        telBot.sendMessage(user_id, 'Km impostati correttamente')
                    else:
                        telBot.sendMessage(user_id, 'Errore durante l\'impostazione dei km')
                else:
                    telBot.sendMessage(user_id, 'Devi specificare i km')
            #do something

        #sleep
        sleep(5)
