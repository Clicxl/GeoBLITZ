import pygame
from pygame.locals import *

BASE_PATH = "Assets/"

def load_img(path):
  img = pygame.image.load(BASE_PATH+path).convert_alpha()
  return img