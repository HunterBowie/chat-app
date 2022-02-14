import pygame
from .util import DEFAULT_FONT

def get_text_size(string, size=30, font_file=pygame.font.get_default_font()):
    t = Text(0, 0, string, font_file, size)
    return t.get_width(), t.get_height()

class Text:
    FONT = DEFAULT_FONT
    def __init__(self, x, y, string, font_file=None,
    size=30, color=(0, 0, 0), alpha=0, antialias=True):
        self.x = x
        self.y = y
        self.string = string
        self.font_file = font_file
        self.size = size
        self.color = color
        self.alpha = alpha
        self.antialias = antialias
        if self.font_file == None:
            self.font_file = self.FONT
        self.font = pygame.font.Font(self.font_file, self.size)
    
    def add(self, string):
        self.string = self.string + string
    
    def pop(self):
        char = self.string[len(self.string)-1]
        self.string = self.string[:len(self.string)-1]
        return char
    
    def get_width(self):
        return self.get_surf().get_width()
    
    def get_height(self):
        return self.get_surf().get_height()
    
    def get_surf(self):
        self.font = pygame.font.Font(self.font_file, self.size)
        return self.font.render(self.string, self.antialias, self.color)
    
    def render(self, screen):
        screen.blit(self.get_surf(), (self.x, self.y))
    
    def center_y(self, rect):
        self.y = rect.center[1]-self.get_height()/2

    def center_x(self, rect):
        self.x = rect.center[0]-self.get_width()/2
    
    def center(self, rect):
        self.center_x(rect)
        self.center_y(rect)
    
    def get(self):
        return self.string
    
    def set(self, string):
        self.string = string
    
    
