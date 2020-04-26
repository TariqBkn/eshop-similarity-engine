import mysql.connector as mysql
db_host="localhost"
db_user="root"
password=""




class DB_connector:
    def connect(self):
        self.mysql_cursor = self.mydb.cursor()
        
    def __init__(self):
        self.mydb = mysql.connect(host=db_host, user=db_user, passwd=password)
        self.mysql_cursor = self.mydb.cursor()
        self.mysql_cursor.execute("use db")

    def run_query(self, query):
        query=query.strip()

        if self.mydb is None:
            self.connect()
            
        if (";" in query):
            raise ValueError("Illegal Arguement, can't use \";\" in your query")
        else:
            self.mysql_cursor.execute(query)
        
        return self.mysql_cursor


