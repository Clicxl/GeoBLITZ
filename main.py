# imports  -------------------------------------------------------------------- #
from scripts.Classes import *

class Game:
  def __init__(self):
    #Setup window/pygame  -------------------------------------------------------- #
    pygame.init()
    self.clock  = pygame.time.Clock()
    self.screen = pygame.display.set_mode(SCREEN,0,32)
    pygame.display.set_caption("GeoBLITZ")

    # Other Variables ------------------------------------------------------------#
    self.Country_Display = pygame.Surface((400,400))
    self.Country_Display.set_colorkey((0,0,0))
    self.Country_Rect = self.Country_Display.get_rect(center=(SCREEN[0]/2,(SCREEN[1]/2)-100))

    self.Start = self.clock.get_time()
    # Sprites And Groups ---------------------------------------------------------#
    self.Country = Country(self)
    self.Country_Group = pygame.sprite.Group()
    self.Country_Group.add(self.Country)

    self.Text = Input(self)
    self.Text_Group = pygame.sprite.Group()
    self.Text_Group.add(self.Text)

    self.Timer = Timer(self)
    self.Timer_group = pygame.sprite.Group()
    self.Timer_group.add(self.Timer)

    self.BG_screen = pygame.Surface((1280,720))
    # self.BG_screen.set_alpha(10)
    # self.BG = load_img("BG.png")
    self.Para_1 = BackGround(self.BG_screen,5,["Assets/Misc/Fill_SQ.png" ,"Assets/Misc/Outline_SQ.png"])
    self.Para_2 = BackGround(self.BG_screen,5,["Assets/Misc/Fill_SQ.png" ,"Assets/Misc/Outline_SQ.png"])
    
    self.prev_time = time.time()
  def run(self):
    # Game Loop ----------------------------------------------------------------- #
    while True:
      # Delta Time
      self.dt = time.time()-self.prev_time
      self.dt *= 60
      self.prev_time = time.time()
      # Background  --------------------------------- ---------------------------- #
      self.screen.fill(BACKGROUND)
      self.BG_screen.fill("Black")
      self.Para_1.update()
      self.Para_2.update()
      self.screen.blit(self.BG_screen,(0,0))
      # Buttons  ---------------------------------------------------------------- #
      for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
          pygame.quit()
          exit()
        self.Text.update(event)
        if event.type == pygame.KEYDOWN:
          if event.key == K_RETURN: 
            self.Text.Input_text = self.Country.check(self.Text.Input_text)
      
      # Sprite Group Update ----------------------------------------------------- #
      self.Country_Group.draw(self.Country_Display)
      self.screen.blit(self.Country_Display,self.Country_Rect)
      
      self.Text_Group.draw(self.screen)
      self.Timer_group.draw(self.screen)
      # Update  ----------------------------------------------------------------- #
      self.Timer_group.update()
      for event in pygame.event.get():
        self.Text_Group.update(event)

      self.clock.tick(60)
      pygame.display.flip()

if __name__ == "__main__":
  Game = Game()
  Game.run()