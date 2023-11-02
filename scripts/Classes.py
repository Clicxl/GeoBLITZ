from scripts.SETTINGS import *
from scripts.utils import *
from scripts.filesSQL import *


class Country(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        # Random Country Selector ---------------------------------------------#
        self.Countries = {}
        self.con_dict()
        self.randCont()
        
        # Sprites -------------------------------------------------------------#
        self.image = load_img(self.Img_path)
        self.image = pygame.transform.scale(self.image, self.game.Country_Display.get_size())
        self.rect = self.image.get_rect()
        self.rect.center = [self.game.Country_Display.get_width() / 2, self.game.Country_Display.get_height() / 2]
        # Chances -------------------------------------------------------------#
        self.chances = 0

    def con_dict(self):
        for image in listdir('Assets/Countries'):
            self.Countries[image.replace(".png", "")] = {"Name": image.replace(".png", "").lower(),"Dir": "Countries/" + image}
        self.Countries_copy = self.Countries.copy()

    def randCont(self):
        self.Con_Keys = list(self.Countries_copy.keys())
        try:
            self.Rand_Cont = random.choice(self.Con_Keys)
            self.Img_path = self.Countries_copy[self.Rand_Cont]["Dir"]
        except:
            self.game.game_state = False
            
    def check(self, Input):
        self.Input = Input.lower()
        if self.Input == self.Countries_copy[self.Rand_Cont]["Name"]:
            self.game.POINTS += 4
            self.Countries_copy.pop(self.Rand_Cont)
            self.chances = 0
            self.redraw_display()
            
        elif self.Input != "":
            self.game.screen_shake.shake()
            self.chances += 1
            if self.chances == 3:
                self.game.POINTS -= 1
                self.Countries_copy.pop(self.Rand_Cont)
                self.redraw_display()
                self.chances = 0

        if self.game.game_state == False:
            print("Entering")
            self.game.Binary.write_score({self.game.ID: {"score": self.game.POINTS}})
            # self.game.SQL.update(self.game.POINTS)
            
        return ""

    def redraw_display(self):
        self.randCont()
        self.game.Country_Display.fill("Black")
        self.image = load_img(self.Img_path)
        self.image = pygame.transform.scale(self.image, self.game.Country_Display.get_size())
        self.image.set_alpha(100)

class Input(pygame.sprite.Sprite):
    def __init__(self, game,color):
        super().__init__()
        self.color = color
        self.game = game
        self.Font = pygame.font.Font("Assets/Fonts/Font.otf", 32)
        # pygame.font.Font("Assets/Fonts/Font.otf", 20)

        # Sprite --------------------------------------------------------------#
        self.image = pygame.Surface((self.game.Country_Display.get_width(),50))
        self.image.fill('Grey')
        
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.game.Country_Rect.left, self.game.Country_Rect.bottom + 100]
        self.Input_text = ""

    def text_input(self, event):
        if event.type == pygame.KEYDOWN and event.key not in [K_RETURN, K_TAB, K_DELETE]:
            if event.key == K_BACKSPACE:
                self.Input_text = self.Input_text[:-1]
            else:
                self.Input_text += event.unicode

    def update(self, event):
        self.image.fill('Grey')
        self.text_input(event)
        self.Font_surf = self.Font.render(self.Input_text,False,(0,0,0))
        self.image.blit(self.Font_surf, (10, 7))

class Timer(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((25, 128))
        self.image.fill("Green")
        self.rect = self.image.get_rect()
        self.rect.midleft = [100, 150]

        self.current_time = 0

    def update(self):
        
        self.current_time = pygame.time.get_ticks() - self.game.Start
        self.ratio = min(60,max(0, TIME - (self.current_time / 1000)))
        self.image = pygame.transform.scale(self.image, (25*3, self.ratio * 15))
        if self.ratio == 0:
            self.game.game_state = False

class BackGround:
    def __init__(self, game, screen, dy, path, angle=-0.55):
        self.Surf_list = []
        self.game = game
        self.dt = time.time() - self.game.prev_time
        self.dt *= 60
        self.path = path
        self.image = pygame.image.load(self.path[0]).convert_alpha()
        self.rect = self.image.get_rect()
        self.da = float(angle)
        self.screen = screen
        self.dy = dy
        self.angle = 0
        self.Surf_draw()

    def Surf_draw(self):
        for i in range(1, 2):
            self.image = pygame.image.load(random.choice(self.path)).convert_alpha()
            self.height = random.randint(30, 150)
            self.image = pygame.transform.scale(self.image, (self.height, self.height))
            pos = [(random.randrange(0, 1280, 75)) * i, random.randrange(0, 720, 75) + 720]
            self.rect.midleft = pos
            self.image.set_alpha(20)
            self.Surf_list.append([self.image, self.rect])

    def blizzard(self):
        for Surf in self.Surf_list:
            self.angle += self.da * self.dt
            Surf[1].y -= self.dy * self.dt
            if Surf[1].y <= 0 - self.image.get_height():
                self.Surf_list.reverse()
                self.Surf_list.remove(Surf)

            Surf_copy = pygame.transform.rotate(Surf[0], self.angle)
            Surf_pos = (Surf[1].x - int(Surf_copy.get_width() / 2), Surf[1].y - int(Surf_copy.get_height() / 2))
            self.screen.blit(Surf_copy, Surf_pos)

    def redraw_lines(self):
        if len(self.Surf_list) == 0:
            self.Surf_draw()

    def update(self):
        self.blizzard()
        self.redraw_lines()

class Font:
    def __init__(self, game):
        # self.FONT = pygame.font.Font(paths("Fonts/"))
        self.game = game

    def type(self, statement,pos,size):
        self.FONT = pygame.font.Font("Assets/Fonts/Font.otf", size)
        self.Font_surf = self.FONT.render(str(statement), False, (255, 255, 255))
        self.Font_rect = self.Font_surf.get_rect()
        self.Font_rect.center = pygame.Vector2(pos)
        self.game.screen.blit(self.Font_surf, self.Font_rect)
        return self.Font_surf

    def update(self, statement):
        self.type(statement)

class Particle:
    def __init__(self,game,colour=[255,200,5]):
        self.dx = 0
        self.dy = 0
        self.particles = []
        self.game = game
        self.colour = colour
        
    def parti_draw(self):
        #Pariticle Variable
        self.velocity = [random.randint(0,20)/10-1,-1]
        self.time = random.randint(5,7)
        self.mouse_pos = pygame.mouse.get_pos()
        
        
        self.particles.append([list(self.mouse_pos),self.velocity,self.time])
        for particle in self.particles:
            
            particle[0][0]+= particle[1][0] + 2 * self.game.dt
            particle[0][1] += particle[1][1] + 4 * self.game.dt
            particle[1][1] += 0.003 * self.game.dt
            particle[2]-= 0.1 * self.game.dt
            pygame.draw.circle(self.game.screen,(225,200,2),[int(particle[0][0]),int(particle[0][1])],int(particle[2]))
            
            
            if particle[2 ] <= 0:
                self.particles.remove(particle)

class Button:
    def __init__(self,game,pos,statement):
        self.game = game
        self.pos = pygame.Vector2(pos)
        self.state = [pygame.transform.scale(pygame.image.load('Assets/Sprites/Button1.png'),(250,75)),pygame.transform.scale(pygame.image.load('Assets/Sprites/Button2.png'),(250,75))]
        self.image = self.state[0]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.clicked = False
        self.statement = statement
        self.Font = Font(self)
        self.screen = self.game.screen 
        self.Font_center = list(self.rect.center)
        self.music = pygame.mixer.Sound("Assets/Music/Click.wav")
        self.music.set_volume(0.7)
        
    def draw(self):
        self.game.screen.blit(self.image,self.rect)
        self.Font.type(self.statement,(self.Font_center[0],self.Font_center[1] - 10),35)
        
        self.mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(self.mouse_pos):
            self.image = self.state[1]
            self.Font_center[1] += 4
            if self.Font_center[1] >= self.rect.center[1] - 4:
                self.Font_center[1]  = self.rect.center[1] + 4
                
            
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.music.play(0)                
                
            if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
                
        else:
            self.image = self.state[0]
            self.Font_center = list(self.rect.center)
    def update(self):
        self.draw()

class ScreenShake:
    def __init__(self,game):
        self.game = game
        self.screen_shake = 0
        self.render_offset = [0,0]
        self.music = pygame.mixer.Sound("Assets/Music/Wrong.wav")
        self.music.set_volume(0.7)
        
    def shake(self):
        """Shakes the screen when something goes wrong"""
        self.screen_shake = 30
        for i in range (self.screen_shake):
                
            if self.screen_shake > 0:
                self.screen_shake -= 1
                
            if self.screen_shake :
                self.render_offset[0] = random.randint(0,32)-16
                self.render_offset[1] = random.randint(0,32)-16
                self.music.play(0)                
                
                
            self.game.screen.fill((191,0,0,50))
            self.game.screen.set_alpha(75)