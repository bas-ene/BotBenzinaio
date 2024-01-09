#imports
from time import sleep
from sqlConnector import sqlConnector
from telegramBot import telegramBot
from ors_service import ors_service
import requests, json

#global conts
PATHTOKENBOT = './data/token_bot.json'
PATHORSTOKEN = './data/ors_token.json'
PATHPRICES = './data/prezzi.csv'
PATHGASPUMPS = './data/anagrafica.csv'
PATHCONFIGDB = './data/db_config.json'

#functions
def readToken(token_path):
    token = ''
    with open(token_path, 'r') as token_file:
        token = json.loads(token_file.read())['token']
    return token

def downloadFile(url, outputFile):
    with requests.get(url) as r:
        outputFile.write(r.text)
        r.close()   
        return r.text

def parseCommand(command):
    command = command.split(' ')
    if(len(command) == 1):
        return [command[0], '']
    else:
        return [command[0], ' '.join(command[1:])]

def parseCsv(csv_lines):
    #format: day of extraction 
    #        list of coloumns
    #        list of data
    #read first line for getting the number of coloumns
    coloumns = csv_lines.split('\n')[1].split(';')
    csv_lines = csv_lines.split('\n')[2:]
    parsed_lines = []
    for line in csv_lines: 
        #split the line
        line = line.split(';')
        #create a new dict
        #check if the line is empty
        if(line == ['']):
            continue
        line_dict = {}
        #for each coloumn
        for i in range(len(coloumns)):
            #add the value to the dict
            line_dict[coloumns[i]] = line[i]
            #add the dict to the list
            parsed_lines.append(line_dict)
    return parsed_lines

def handleMessage(message_data, db_conn = sqlConnector(PATHCONFIGDB), telBot = telegramBot(readToken(PATHTOKENBOT))):
        command = parseCommand(message_data)
        if not command: 
            telBot.sendMessage(user_id, 'Per favore inserisci un valore per il comando')
            return
        match command[0]:            
            case '/help':
                telBot.sendHelp(user_id)
            case '/carburante':
                success = db_conn.setGasType(user_id, command[1])
                if(success):
                    telBot.sendMessage(user_id, 'Carburante impostato correttamente')
                else:
                    telBot.sendMessage(user_id, 'Errore durante l\'impostazione del carburante, potrebbe non essere nel nostro database')
            case '/consumo':
                success = db_conn.setEfficiency(user_id, command[1])
                if(success):
                    telBot.sendMessage(user_id, 'Consumo impostato correttamente')
                else:
                    telBot.sendMessage(user_id, 'Errore durante l\'impostazione del consumo')
            case '/serbatoio':
                success = db_conn.setTankCapacity(user_id, command[1])
                if(success):
                    telBot.sendMessage(user_id, 'Serbatoio impostato correttamente')
                else:
                    telBot.sendMessage(user_id, 'Errore durante l\'impostazione del serbatoio')
            case '/km':
                success = db_conn.setMaxKm(user_id, command[1])
                if(success):
                    telBot.sendMessage(user_id, 'Km impostati correttamente')
                else:
                    telBot.sendMessage(user_id, 'Errore durante l\'impostazione dei km')
            case _: 
                telBot.sendMessage(user_id, 'Comando non riconosciuto')

def handleLocation(location_data, user, ors = ors_service(readToken(PATHORSTOKEN)), db_conn = sqlConnector(PATHCONFIGDB)):
    #get the gas pumps near the location
    gas_pumps = db_conn.getGasPumpsNearUser(location_data, 10, user)
    
    min_distance = 100000
    nearest_gas_pump = None
    min_price = 100000
    cheapest_gas_pump = None
    dict_distances = {}
    for gas_pump in gas_pumps:
        #get real distance from user if not already calculated
        if (gas_pump[0] not in dict_distances):
            distance = ors.getDistance(ors.getDirections(location_data, { 'longitude': gas_pump[9], 'latitude': gas_pump[8]}))
            dict_distances[gas_pump[0]] = distance
        else:
            distance = dict_distances[gas_pump[0]]
        #add distance to the dict
        #get nearest
        if(distance < min_distance):
            min_distance = distance
            nearest_gas_pump = gas_pump
        #get most convenient
        print(distance)
    print(nearest_gas_pump)

#main func
if __name__ == "__main__":

    #download updated prices and details about gas pumps
    #create sql connection
    print("connecting to database")
    db_conn = sqlConnector(PATHCONFIGDB)
    
    # with open(PATHPRICES, 'w') as file_prices:
    #     print('downloading prices')
    #     csv_data_prices = downloadFile('https://www.mimit.gov.it/images/exportCSV/prezzo_alle_8.csv', file_prices)
    #     parsed_data = parseCsv(csv_data_prices)
    #     for data in parsed_data:
    #         del data['dtComu']
    #     db_conn.loadPrices(parsed_data)
    #
    # with open(PATHGASPUMPS, 'w') as file_gas_pumps:
    #     print('downloading gas pumps details')
    #     csv_data_gaspumps = downloadFile('https://www.mimit.gov.it/images/exportCSV/anagrafica_impianti_attivi.csv', file_gas_pumps)
    #     print('loading gas pumps details in database')
    #     db_conn.loadGasPumps(parseCsv(csv_data_gaspumps))

    #get bot 
    telBot = telegramBot(readToken(PATHTOKENBOT))

    #get ors service
    ors = ors_service(readToken(PATHORSTOKEN))

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
            if(db_conn.getUser(user_id) == []):
                print('new user')
                #insert new user
                db_conn.insertUser(user_id, username)
                telBot.setUpNewUser(user_id)
            else:
                print('old user')
            
            #get the type of message
            message_data = message['message']
            print(message_data)
            if 'location' in message_data:
                handleLocation(message_data['location'], user_id, ors, db_conn)
            elif 'text' in message_data:
                handleMessage(message_data['text'], db_conn, telBot)
            #do something

        #sleep
        sleep(5)
