from subprocess import run
import pygame
from pygame.locals import *
from os import listdir

def req(file):
    command = ["pip","install","-r",file]
    run(command)

BASE_PATH = "Assets/"

def load_img(path):
    img = pygame.image.load(BASE_PATH + path).convert_alpha()
    return img

def load_imgs(path_list):
    img_list = []
    for i in path_list:
        img = load_img(i)
        img_list.append(img)
    return img_list

def paths(subfolders):
    for i in range(1, 2):
        paths = list(BASE_PATH + subfolders + img for img in listdir(BASE_PATH + subfolders))
    return paths

def sprite_sheet(image,size):
    sprite_sheet = load_img(image)
    surf = pygame.Surface(size).convert_alpha()
    
    return image