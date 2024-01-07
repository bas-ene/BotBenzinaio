import mysql.connector
import json
class sqlConnector:

    def __init__(self, config_file_path):
        with open(config_file_path) as config_file:
            config = json.load(config_file)
            self.mydb = mysql.connector.connect(
                host=config['host'],
                user=config['user'],
                password=config['password'],
                database=config['database']
            )
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute('SELECT DISTINCT tipo FROM users')
        self.carburanti = self.mycursor.fetchall()
    
    def getUser(self, chat_id):
        self.mycursor.execute(f'SELECT * FROM users WHERE userId = {chat_id}')
        myresult = self.mycursor.fetchall()
        return myresult
    
    def insertUser(self, user_id, username):
        sql = "INSERT INTO users (userId, username) VALUES (%s, %s)"
        val = (user_id, username)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        print(self.mycursor.rowcount, "record inserted.")

    def setGasType(self, chat_id, gas):
        # if carburante not in self.carburanti:
        #     return False
        sql = f"UPDATE users SET tipo = '{gas.lower()}' WHERE userId = {chat_id}"
        self.mycursor.execute(sql)
        self.mydb.commit()
        print(self.mycursor.rowcount, "record(s) affected")
        return True
    
    def setEfficiency(self, chat_id, efficiency):
        if(efficiency.find(',') != -1):
            efficiency = efficiency.replace(',', '.')
        efficiency = float(efficiency)
        sql = f"UPDATE users SET consumo = {efficiency} WHERE userId = {chat_id}"
        self.mycursor.execute(sql)
        self.mydb.commit()
        print(self.mycursor.rowcount, "record(s) affected")
        return True
    
    def setTankCapacity(self, chat_id, capacity):
        if(capacity.find(',') != -1):
            capacity = capacity.replace(',', '.')
        capacity = float(capacity)
        sql = f"UPDATE users SET capacita = {capacity} WHERE userId = {chat_id}"
        self.mycursor.execute(sql)
        self.mydb.commit()
        print(self.mycursor.rowcount, "record(s) affected")
        return True

    def setMaxKm(self, chat_id, maxKm):
        if(maxKm.find(',') != -1):
            maxKm = maxKm.replace(',', '.')
        maxKm= float(maxKm)
        sql = f"UPDATE users SET maxkm = {maxKm} WHERE userId = {chat_id}"
        self.mycursor.execute(sql)
        self.mydb.commit()
        print(self.mycursor.rowcount, "record(s) affected")
        return True
    
    def getMaxKm(self, chat_id):
        sql = f"SELECT maxkm FROM users WHERE userId = {chat_id}"
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        return myresult[0][0]

    def loadGasPumps(self, data):
        sql = "INSERT INTO gaspumps (idImpianto, gestore, bandiera, tipo, nome, indirizzo, comune, provincia, latitudine, longitudine) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        for gas_pump in data:
            for field in gas_pump:
                if(field == ''):
                    field = 'NULL'
            print(gas_pump)
            try:
                print('inserting in db')
                val = [gas_pump['idImpianto'], gas_pump['Gestore'], gas_pump['Bandiera'], gas_pump['Tipo Impianto'], gas_pump['Nome Impianto'], gas_pump['Indirizzo'], gas_pump['Comune'], gas_pump['Provincia'], gas_pump['Latitudine'], gas_pump['Longitudine']]
                print('executing query')
                self.mycursor.execute(sql, val)
                print('committing')
                self.mydb.commit()
                print(self.mycursor.rowcount, "record inserted.")
            except Exception as e: 
                print('error inserting in db')
                print(e)
        print('finished loading gas pumps in db')

    def loadPrices(self, data):
        sql = "INSERT INTO prices (idImpianto, descCarburante, prezzo, isSelf) VALUES (%s, %s, %s,%s)"
        for price in data:
            for field in price:
                if(field == ''):
                    field = 'NULL'
            print(price)
            try:
                print('inserting in db')
                val = [price['idImpianto'], price['descCarburante'], price['prezzo'], price['isSelf']]
                print('executing query')
                self.mycursor.execute(sql, val)
                print('committing')
                self.mydb.commit()
                print(self.mycursor.rowcount, "record inserted.")
            except Exception as e:
                print('error inserting in db')
                print(e)
        print('finished loading prices in db')
    
    def getGasPumpsNearUser(self, longitude, latitude,  num_results):
        sql = f'''SELECT *, SQRT(POW(latitudine - {latitude}, 2) + POW(longitudine - {longitude},2)) AS dist 
        FROM gaspumps 
        ORDER BY dist ASC
        LIMIT {num_results}
        '''
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        return myresult
