# Imports  -------------------------------------------------------------------- #
import pygame ,time
from pygame.locals import *
from sys import exit
import random
from os import listdir
import pickle 
import mysql.connector as sql

# Constants  ----------------------------------------------------------------- #
BACKGROUND = (200,200,200)
SCREEN = (1280,720)
FPS = 60
TIME = 30 # (sec)
