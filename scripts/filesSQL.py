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
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.table} (
                            player_id VARCHAR(50) PRIMARY KEY,player_name VARCHAR(50) NOT NULL,
                            points INTEGER)''')
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

    def check_login(self,username, password):
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = self.cursor.fetchone()
        if user:
            return True
        return False

    # Function to display text on screen
    def text_objects(self,text, font):
        text_surface = font.render(text, True,(128, 128, 128))
        return text_surface, text_surface.get_rect()

    # Function to display message
    def message_display(self,text):
        large_text = pygame.font.Font(None, 30)
        text_surf, text_rect = self.text_objects(text, large_text)
        text_rect.center = (200, 150)
        self.game.screen.blit(text_surf, text_rect)

    # Function for the login screen
    def login_screen(self):
        login = ''
        password = ''
        login_input = False
        password_input = False

        while True:
            self.game.screen.fill((255,255,255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Check login when Enter is pressed
                        if self.check_login(login, password):
                            self.message_display('Login successful!')
                        else:
                            self.message_display('Invalid login credentials.')

                        login = ''
                        password = ''

                    elif login_input:
                        if event.key == pygame.K_BACKSPACE:
                            login = login[:-1]
                        else:
                            login += event.unicode

                    elif password_input:
                        if event.key == pygame.K_BACKSPACE:
                            password = password[:-1]
                        else:
                            password += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 150 < x < 250 and 80 < y < 100:
                        login_input = True
                        password_input = False
                    elif 150 < x < 250 and 140 < y < 160:
                        login_input = False
                        password_input = True

            # Draw login and password input boxes
            pygame.draw.rect(self.game.screen,(128, 128, 128), (150, 80, 100, 20), 2)
            pygame.draw.rect(self.game.screen,(128, 128, 128), (150, 140, 100, 20), 2)

            # Display login and password texts
            text_surface = pygame.font.Font(None, 30).render(login, True,(128, 128, 128))
            self.game.screen.blit(text_surface, (155, 82))

            text_surface = pygame.font.Font(None, 30).render('*' * len(password), True,(128, 128, 128))
            self.game.screen.blit(text_surface, (155, 142))
