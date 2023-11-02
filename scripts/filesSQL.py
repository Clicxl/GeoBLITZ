from scripts.SETTINGS import *
from .Classes import *

class BinaryFile:
    def __init__(self, game, file_name):
        self.file_name = file_name
        self.game = game

    def write_score(self, data):
        with open(self.file_name, 'ab') as file:
            pickle.dump(data,file)

    def read_scores(self):
        scores = []
        with open(self.file_name, 'rb') as file:
            while True:
                try:
                    data = pickle.load(file) 
                    if not data:
                        break
                    scores.append((data[0], data[1]))
                except EOFError:
                    pass
        return scores
    
class SQL:
    def __init__(self,game,password,player_id,username='root',host='localhost',database="Globule"):
        self.conn = sql.connect(host=host,user=username,password=password,auth_plugin = "mysql_native_password")
        self.cursor = self.conn.cursor()
        self.db = "Globule"
        self.table = "Points"
        self.game = game
        self.player_id = player_id
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db}")
        self.conn.commit()
        self.cursor.execute(f"USE {self.db}")
        
        self.create_table()
        
    def create_table(self):
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.table} (
                            player_id VARCHAR(50),points INTEGER)''')
        self.conn.commit()

    def add_points(self, points):
        self.cursor.execute(f"INSERT INTO {self.table} values({self.player_id},{points})")
        self.conn.commit()
            
    def update(self,points):
        self.add_points(points)
        self.conn.close()
        

