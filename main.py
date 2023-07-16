# imports  -------------------------------------------------------------------- #
import pygame 
from pygame.locals import *
from sys import exit
from SETTINGS import *
from Classes import *

#Setup window/pygame  -------------------------------------------------------- #
pygame.init()
clock  = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN,0,32)
pygame.display.set_caption("GeoBLITZ")

# Other Variables ------------------------------------------------------------#
Country_Display = pygame.Surface((400,400))
Country_Display.fill("White")
Country_Rect = Country_Display.get_rect(center=(SCREEN[0]/2,(SCREEN[1]/2)-100))

Start = 0
# Sprites And Groups ---------------------------------------------------------#
Country = Country(Country_Display)
Country_Group = pygame.sprite.Group()
Country_Group.add(Country)

Text = Input(Country_Display,Country_Rect)
Text_Group = pygame.sprite.Group()
Text_Group.add(Text)

Timer = Timer(Start)
Timer_group = pygame.sprite.Group()
Timer_group.add(Timer)

# Game Loop ----------------------------------------------------------------- #
while True:
  # Background  ------------------------------------------------------------- #
  screen.fill('White')
  
  # Buttons  ---------------------------------------------------------------- #
  for event in pygame.event.get():
    if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
      pygame.quit()
      exit()
    Text.update(event)
    if event.type == pygame.KEYDOWN:
      if event.key == K_RETURN: 
        Text.Input_text = Country.check(Text.Input_text)
  
  # Sprite Group Update ----------------------------------------------------- #
  Country_Group.draw(Country_Display)
  screen.blit(Country_Display,Country_Rect)
  
  Text_Group.draw(screen)
  Timer_group.draw(screen)
  # Update  ----------------------------------------------------------------- #
  Timer_group.update()
  
  for event in pygame.event.get():
    Text_Group.update(event)
  clock.tick(60)
  pygame.display.flip()