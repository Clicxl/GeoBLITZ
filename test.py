import pygame,sys

pygame.init()
clock  = pygame.time.Clock()
screen = pygame.display.set_mode((500,500),0,32)
Font = pygame.font.SysFont("Roboto",32)
Input_text =""
# Game Loop ----------------------------------------------------------------- #
while True:
  # Background  ------------------------------------------------------------- #
  screen.fill('White')

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()
      if event.key == pygame.K_BACKSPACE:
        Input_text = Input_text[:-1]
      else:
        Input_text += event.unicode

  text_surf = Font.render(Input_text,True,(0,0,0))      
  screen.blit(text_surf,(0,0))
  clock.tick(60)
  pygame.display.flip()