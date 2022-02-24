import pygame
pygame.init()
from chatapp.constants import Constants

screen = pygame.display.set_mode(Constants.SCREEN_SIZE)
screen.fill((255, 255, 255))

from chatapp.app import App

app = App()

app.start()