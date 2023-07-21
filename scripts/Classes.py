from scripts.SETTINGS import *
from scripts.utils import *
class Country(pygame.sprite.Sprite):
  def __init__(self,game):
    super().__init__()
    self.game = game
    # Random Country Selector ---------------------------------------------#
    self.Countries = {}
    self.con_dict()
    self.randCont()
    # Sprites -------------------------------------------------------------#
    self.image = load_img(self.Img_path)
    self.image = pygame.transform.scale(self.image,self.game.Country_Display.get_size())
    self.rect = self.image.get_rect()
    self.rect.center = [self.game.Country_Display.get_width()/2,self.game.Country_Display.get_height()/2]
    
  def con_dict(self):
    for image in listdir('Assets/Countries'):
      self.Countries[image.replace(".png","")] = {"Name":image.replace(".png","").lower(),"Dir":"Countries/"+image}
    self.Countries_copy = self.Countries.copy()

  def randCont(self):
    self.Con_Keys = list(self.Countries_copy.keys())
    try:
      self.Rand_Cont = random.choice(self.Con_Keys)
      self.Img_path = self.Countries_copy[self.Rand_Cont]["Dir"]
    except:
      print('Game Options over')
      


  def check(self,Input):
    self.Input = Input.lower()
    if self.Input == self.Countries_copy[self.Rand_Cont]["Name"]:
      self.Countries_copy.pop(self.Rand_Cont)
      self.redraw_display()
    else:
      print("Wrong")
    return ""

  def redraw_display(self):
      self.randCont()
      self.game.Country_Display.fill("Black")
      
      self.image = load_img(self.Img_path)
      self.image = pygame.transform.scale(self.image,self.game.Country_Display.get_size())

class Input(pygame.sprite.Sprite):
  def __init__(self,game):
    super().__init__()
    self.game = game
    self.Font = pygame.font.SysFont("Arial",32)
    # Sprite --------------------------------------------------------------#
    self.image = pygame.Surface((self.game.Country_Display.get_width(),50))
    self.image.fill('Red')
    self.rect = self.image.get_rect()
    self.rect.topleft = [self.game.Country_Rect.left,self.game.Country_Rect.bottom+100]

    self.Input_text = ""

  def text_input(self,event):
    if event.type == pygame.KEYDOWN:
      if event.key not in [K_RETURN,K_TAB,K_DELETE]:
        if event.key == K_BACKSPACE:
          self.Input_text = self.Input_text[:-1]
        else:
          self.Input_text += event.unicode

  def update(self,event):
    self.image.fill('Red')
    self.text_input(event)
    self.Font_surf = self.Font.render(self.Input_text,False,(0,0,0))
    self.image.blit(self.Font_surf,(10,7))

class Timer(pygame.sprite.Sprite):
  def __init__(self,game):
    super().__init__()
    self.game = game
    self.image = pygame.Surface((300,25))
    self.image.fill("Blue")
    self.rect = self.image.get_rect()
    self.rect.midleft = [450,650]
    
    self.current_time = 0
    
  def update(self):
    self.current_time = pygame.time.get_ticks() - self.game.Start
    self.ratio = max(0,TIME-(self.current_time/1000))
    self.image = pygame.transform.scale(self.image,(self.ratio*30,60))
    if self.ratio == 0:
      self.game.screen.blit(self.game.BG_screen,(0,0))

class BackGround:
  def __init__(self,screen,dy,path,angle=-0.55):
    self.Surf_list = []
    self.path = path
    self.image = pygame.image.load(self.path[0]).convert_alpha()
    self.rect = self.image.get_rect()
    self.da = float(angle)
    self.screen = screen
    self.dy = dy
    self.angle = 0
    self.Surf_draw()

  def Surf_draw(self):
    for i in range(0,1):
      self.image = pygame.image.load(random.choice(self.path)).convert_alpha()      
      self.height = random.randint(30,150)
      self.image = pygame.transform.scale(self.image,(self.height,self.height))
      pos = [random.randrange(0,1280,75),random.randrange(0,720,75)+720]
      self.rect.midleft = pos
      self.image.set_alpha(20)
      self.Surf_list.append([self.image,self.rect])

  def blizard(self):
    for Surf in self.Surf_list:
      self.angle += self.da
      Surf[1].y -= self.dy
      if Surf[1].y <= 0-self.image.get_height():
        self.Surf_list.reverse()
        self.Surf_list.remove(Surf)
        
      Surf_copy = pygame.transform.rotate(Surf[0],self.angle)
      Surf_pos = (Surf[1].x - int(Surf_copy.get_width()/2) , Surf[1].y - int(Surf_copy.get_height()/2))
      self.screen.blit(Surf_copy,Surf_pos)

  def redraw_lines(self):
    if len(self.Surf_list) == 0:
      self.Surf_draw()

  def update(self):
    self.blizard()
    self.redraw_lines()