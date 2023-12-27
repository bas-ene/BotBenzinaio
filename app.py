#imports
import requests
import time
import sched
#global vars
path_bottoken = './token_bot.txt'
url_bot_telegram = 'https://api.telegram.org/bot'

#functions
def getBotEndpoint():
    bot_token = ''
    with open(path_bottoken, 'r') as bot_token_file:
        bot_token = bot_token_file.read()
    return f'{url_bot_telegram}{bot_token}'

def downloadFile(url, outputFile):
    r = requests.get(url)
    outputFile.write(r.text)
    r.close()

#main func
if __name__ == "__main__":
    #read and create connection to telegram bot
    ENDPOINT = getBotEndpoint()   
    
    scheduler =     scheduler = sched.scheduler(time.time, time.sleep)

    #download updated prices and details about gas pumps
    file_prezzi = open('prezzi.csv', 'w')
    downloadFile('https://www.mimit.gov.it/images/exportCSV/prezzo_alle_8.csv', file_prezzi)
    file_anagrafica = open('anagrafica.csv', 'w')
    downloadFile('https://www.mimit.gov.it/images/exportCSV/anagrafica_impianti_attivi.csv', file_anagrafica)
