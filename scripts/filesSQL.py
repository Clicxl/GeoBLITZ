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
                data = pickle.load(file) 
                if not data:
                    break
                scores.append((data[0], data[1]))
        return scores
    
class SQL:
    def __init__(self,game,password,username='root',host='localhost'):
        self.conn = sql.connect(host=host,user=username,password=password)
        self.create_table()
        self.cursor = self.conn.cursor()
        self.db = "Globue"
        self.table = "Points"
        self.game = game
        
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db}")
        self.conn.commit()
        self.cursor.execute(f"USE {self.db}")
        self.create_table()
        
    def create_table(self):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table} (
                            player_id INTEGER PRIMARY KEY,
                            points INTEGER
                            )")
        self.conn.commit()

    def add_points(self, player_id, points):
        self.cursor.execute(f"INSERT INTO {self.table} values(player_id,points)")
        self.conn.commit()

    def update_points(self, player_id, points):
        self.cursor.execute(f"UPDATE {self.table} SET points = ? WHERE player_id = ?", (points, player_id))
        self.conn.commit()

    def get_points(self, player_id):
        self.cursor.execute(f"SELECT points FROM {self.table} WHERE player_id = player_id")
        points = self.cursor.fetchone()
        return points[0] if points else None

    def close_connection(self):
        self.conn.close()


