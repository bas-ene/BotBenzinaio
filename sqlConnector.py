import mysql.connector
import json
class sqlConnector:

    def __init__(self):
        with open('./db_config.json') as config_file:
            config = json.load(config_file)
            self.mydb = mysql.connector.connect(
                host=config['host'],
                user=config['user'],
                password=config['password'],
                database=config['database']
            )
            self.mycursor = self.mydb.cursor()
    
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
