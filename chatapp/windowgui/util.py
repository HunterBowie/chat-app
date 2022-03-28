from turtle import color
import pygame
from os import path
from .constants import Constants
from .timers import RealTimer

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
    LIGHT_YELLOW = (200, 200, 0)
    LIGHT_RED = (255, 50, 50)
    LIGHT_GREEN = (50, 200, 50)

def get_surf(size, color, alpha):
    surf = pygame.Surface(size, pygame.SRCALPHA)
    surf.fill(color)
    surf.set_alpha(alpha)
    return surf


def render_border(surface, rect, size):
    pygame.draw.line(surface, Colors.BLACK, rect.topleft, rect.topright, size)
    pygame.draw.line(surface, Colors.BLACK, rect.topleft, rect.bottomleft, size)
    pygame.draw.line(surface, Colors.BLACK, rect.bottomleft, rect.bottomright, size)
    pygame.draw.line(surface, Colors.BLACK, rect.topright, rect.bottomright, size)


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


    

def load_img(img_name, img_path, ext=".png", colorkey=None, convert=False, scale=None):
    full_path = path.join(img_path, img_name) + ext
    try:
        img = pygame.image.load(full_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"no image for path {full_path}")
    if scale is not None:
        img = pygame.transform.scale(img, scale)
    if convert:
        img = img.convert()
    if colorkey:
        img.set_colorkey(Colors.BLACK)
    return img


class Flash:
    def __init__(self, x, y, text, size, color, duration=3):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.size = size
        self.alpha = 0
        self._surf_init()

        self.timer = RealTimer()
        self.duration = duration
    
    def start(self):
        self.timer.start()
    
    def _surf_init(self):
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface.fill(self.color)
        self.text.center(self.surface.get_rect())
        self.text.render(self.surface)
        self.surface.set_alpha(self.alpha)
    
    def _surf_fade_in(self):
        if self.alpha < 255:
            self.alpha += Constants.FLASH_FADE_SPEED
            self.surface.set_alpha(self.alpha)
    
    def _surf_fade_out(self):
        if self.alpha > 0:
            self.alpha -= Constants.FLASH_FADE_SPEED
            self.surface.set_alpha(self.alpha)
    
    def is_finished(self):
        return self.timer.passed(self.duration)
    
    def render(self, surface):
        if self.timer.get() < Constants.FLASH_FADE_TIME:
            self._surf_fade_in()
        elif self.duration-self.timer.get() < Constants.FLASH_FADE_TIME:
            self._surf_fade_out()
        surface.blit(self.surface, (self.x, self.y))