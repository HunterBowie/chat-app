import pygame
from os import path

class Colors:
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	RED = (255, 0, 0)
	GREEN = (0, 255, 0)
	BLUE = (0, 0, 255)
	YELLOW = (255, 255, 0)
	ORANGE = (255, 100, 0)
	PURPLE = (150, 50, 250)
	GOLD = (200, 200, 30)
	GREY = (128, 128, 128)


def draw_border(surface, rect, size):
    pass


def root_rect(screen_size, rect, top_y=False, bottom_y=False,
    left_x=False, right_x=False, center_x=False, center_y=False):
    center_pos = int(screen_size[0]/2), int(screen_size[1]/2)
    new_x, new_y = 0, 0
    if center_x:
        new_x = center_pos[0]-int(rect.width/2)
    if center_y:
        new_y = center_pos[1]-int(rect.height/2)
    if left_x:
        new_x = 0
    if right_x:
        new_x = screen_size[0]-rect.width
    if bottom_y:
        new_y = screen_size[1]-rect.height
    if top_y:
        new_y = 0
    rect.x += new_x
    rect.y += new_y
    return rect.x, rect.y



    












