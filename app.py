#imports
from time import sleep
from sqlConnector import *
import requests, json
#global vars
path_bottoken = './token_bot.json'
url_bot_telegram = 'https://api.telegram.org/bot'

#functions
def getBotEndpoint():
    bot_token = ''
    with open(path_bottoken, 'r') as bot_token_file:
        bot_token = json.loads(bot_token_file.read())['token']
    return f'{url_bot_telegram}{bot_token}'

def downloadFile(url, outputFile):
    with requests.get(url) as r:
        outputFile.write(r.text)
        r.close()   
        return r.text


#main func
if __name__ == "__main__":
   
    #download updated prices and details about gas pumps
    # with open('prezzi.csv', 'w') as file_prezzi:
    #     csv_data_prezzi = downloadFile('https://www.mimit.gov.it/images/exportCSV/prezzo_alle_8.csv', file_prezzi)
    # with open('anagrafica.csv', 'w') as  file_anagrafica :
    #     csv_data_anag = downloadFile('https://www.mimit.gov.it/images/exportCSV/anagrafica_impianti_attivi.csv', file_anagrafica)
    #create sql connection
    conn = sqlConnector()
    #put the csv info in the 

    #get bot endpoint
    ENDPOINT = getBotEndpoint()   
    offset = 0
    url_get_updates = f'{ENDPOINT}/getUpdates'
    while True:
        #get new messages
        params = {'offset': offset}
        response = requests.get(url_get_updates, params)
        data = response.json()
        #update offset
        if(len(data['result']) != 0):
            offset=(data['result'][len(data['result'])-1]['update_id']) + 1
        #for each message
        for message in data['result']:
            user_id = message['message']['from']['id']
            username = message['message']['from']['username']
            #get if is a new user
            if(conn.getUser(user_id) == []):
                print('new user')
                #insert new user
                conn.insertUser(user_id, username)
            else:
                print('old user')
            #get the type of message
            
            #do something

        #sleep
        sleep(5)
