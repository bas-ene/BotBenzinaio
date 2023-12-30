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
                threading.Thread(target=telBot.setUpNewUser, args=(user_id, 0)).start()
            else:
                print('old user')
            #get the type of message
            
            #do something

        #sleep
        sleep(5)
