# imports  -------------------------------------------------------------------- #
from scripts.Classes import *
from scripts.filesSQL import *


class Game:
    def __init__(self):
        # Setup window/pygame  -------------------------------------------------------- #
        pygame.init()
        pygame.mixer.pre_init(44100,-16,2,512)
        self.clock = pygame.time.Clock()
        self.main_screen = pygame.display.set_mode(SCREEN, 0, 32)
        self.screen = pygame.Surface(self.main_screen.get_size())
        pygame.display.set_caption("Globule")
        pygame.mouse.set_visible(False)
        # Other Variables ------------------------------------------------------------#
        self.Country_Display = pygame.Surface((400, 400))
        self.Country_Display.set_colorkey((0, 0, 0))
        self.Country_Rect = self.Country_Display.get_rect(center=(SCREEN[0] / 2, (SCREEN[1] / 2) - 100))
        self.POINTS = 0

        self.game_state = "menu"
        # Sprites And Groups ---------------------------------------------------------#
        self.Country = Country(self)
        self.Country_count = len(self.Country.Con_Keys) * 10
        self.Country_Group = pygame.sprite.Group()
        self.Country_Group.add(self.Country)

        self.Text = Input(self,'Grey')
        self.Text_Group = pygame.sprite.Group()
        self.Text_Group.add(self.Text) 
        
        self.Timer = Timer(self)
        self.Timer_group = pygame.sprite.Group()
        self.Timer_group.add(self.Timer)
        self.prev_time = time.time()

        # Classes Import 
        self.BG_screen = pygame.Surface((1280, 720))
        self.Para_1 = BackGround(self, self.BG_screen, 5, paths("Misc/"), 3)
        self.Para_2 = BackGround(self, self.BG_screen, 5, paths("Misc/"), -3)
        self.Para_3 = BackGround(self, self.BG_screen, 5, paths("Misc/"), 4)
        self.Typing = Font(self)
        self.particles = Particle(self)
        self.play = Button(self, (self.screen.get_width() / 2, (3 * self.screen.get_height() / 5) - 16), "Play")
        self.credits = Button(self,(self.screen.get_width()/2,(6*self.screen.get_height()/8)-16),"Credits")
        self.exit = Button(self, (self.screen.get_width() / 2, (9 * self.screen.get_height() / 10) - 16), "Exit")
        self.screen_shake = ScreenShake(self)
        self.Binary = BinaryFile(self, "Assets/Data/Data.dat")

        self.ID = ID()
        # self.SQL = SQL(self,"root",int(self.ID))
        # Music
        pygame.mixer.music.load("Assets/Music/Main_Song.wav")
        # pygame.mixer.music.set_volume(0.025)
        pygame.mixer.music.play(-1)

    def game(self):
        # Game Loop ----------------------------------------------------------------- #
        while True:
            # Delta Time
            self.dt = time.time() - self.prev_time
            self.dt *= 60
            self.prev_time = time.time()

            # Background  -------------------------------------------------------------- #
            self.screen.fill(BACKGROUND)
            self.BG_screen.fill("Black")
            self.Para_1.update()
            self.Para_2.update()
            self.Para_3.update()
            self.screen.blit(self.BG_screen, (0, 0))

            # Buttons  ---------------------------------------------------------------- #
            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE] and self.game_state in [
                    'game', 'menu', False]:
                    pygame.quit()
                    exit()
                self.Text.update(self.event)
                if pygame.key.get_pressed()[pygame.K_ESCAPE] and self.game_state in ['credits']:
                    self.game_state = 'menu'
                if self.event.type == pygame.KEYDOWN:
                    if self.event.key == K_RETURN:
                        self.Text.Input_text = self.Country.check(self.Text.Input_text)

                # Sprite Group Update ----------------------------------------------------- #
            if self.game_state == 'game':
                self.Country_Group.draw(self.Country_Display)
                self.screen.blit(self.Country_Display, self.Country_Rect)

                self.Text_Group.draw(self.screen)
                self.Timer_group.draw(self.screen)
                

                # Update  ----------------------------------------------------------------- #
                self.Timer_group.update()
                self.Text_Group.update(self.event)
                

            if self.game_state == 'menu':
                self.menu()
            if self.game_state == False:
                self.Typing.type(f"Your Points are: {str(self.POINTS)}",(self.screen.get_width() / 2, self.screen.get_height() / 2), 64)
                
            if self.game_state == "credits":
                self.Typing.type('''Special Thanks to the following websites for their invaluable resources: \n
- Country Outline Images: https://www.worldmapsonline.com
- Pixel Art Graphics: Self Made
- Sound Effects and Music: Self Made
- Pygame Tutorials: https://www.youtube.com/@DaFluffyPotato

We greatly appreciate the contributions of these websites and their dedication \nto sharing knowledge and assets,making this \nproject possible.''',(self.screen.get_width()/2,self.screen.get_height()/2),17)

            self.particles.parti_draw()
            self.main_screen.blit(self.screen, self.screen_shake.render_offset)
            self.screen_shake.render_offset = [0, 0]
            self.clock.tick(120)
            pygame.display.flip()

    def menu(self):

        self.Typing.type("Globule", (self.screen.get_width() / 2, self.screen.get_height() / 3), 64)
        self.play.draw()
        self.credits.draw()
        self.exit.draw()

        if self.play.clicked == True:
            self.game_state = 'game'
            self.Start = self.clock.get_time()
        elif self.credits.clicked == True:  
            self.game_state = 'credits'
        elif self.exit.clicked == True:
            pygame.quit()
            exit()

    def run(self):
        self.game()

if __name__ == "__main__":
    Game = Game()
    Game.run()