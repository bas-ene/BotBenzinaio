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

    def setCarburante(self, chat_id, carburante):
        # if carburante not in self.carburanti:
        #     return False
        sql = f"UPDATE users SET tipo = '{carburante.lower()}' WHERE userId = {chat_id}"
        self.mycursor.execute(sql)
        self.mydb.commit()
        print(self.mycursor.rowcount, "record(s) affected")
        return True
    
    def setConsumo(self, chat_id, consumo):
        if(consumo.find(',') != -1):
            consumo = consumo.replace(',', '.')
        consumo = float(consumo)
        sql = f"UPDATE users SET consumo = {consumo} WHERE userId = {chat_id}"
        self.mycursor.execute(sql)
        self.mydb.commit()
        print(self.mycursor.rowcount, "record(s) affected")
        return True
    
    def setSerbatoio(self, chat_id, capacita):
        if(capacita.find(',') != -1):
            capacita = capacita.replace(',', '.')
        capacita = float(capacita)
        sql = f"UPDATE users SET capacita = {capacita} WHERE userId = {chat_id}"
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
