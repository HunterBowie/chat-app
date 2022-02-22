import pygame
from .assets import Assets



class Text:
    default_font_name = "regular"
    def __init__(self, x, y, string, font_name=None,
    size=30, color=(0, 0, 0), alpha=0, antialias=True, max_width=None):
        self.x = x
        self.y = y
        self.string = string
        self.size = size
        self.color = color
        self.alpha = alpha
        self.antialias = antialias
        self.font_name = font_name
        if self.font_name is None:
            self.font_name = self.default_font_name
        self.font_file = Assets.FONTS[self.font_name]
        self.font = pygame.font.Font(self.font_file, self.size)
        self.max_width = max_width


    def set(self):
        self.lines = [self.string]
        if self.max_width:
            if Text(0, 0, self.string).get_width() > self.max_width:
                current_string = self.string

                while Text(0, 0, current_string).get_width() > self.max_width:
                    pass


    
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
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.get_width(), self.get_height())
    
    def get_surf(self):
        self.font = pygame.font.Font(self.font_file, self.size)

        renders = []    
        for string in self.lines:
            self.renders.append(self.font.render(string, self.antialias, self.color))
        
        width = height = 0
        for surf in renders:
            width += surf.get_width()
            height += surf.get_height()
        
        full_surf = pygame.Surface((width, height))
        x = y = 0
        for surf in renders:
            full_surf.blit(surf, (x, y))
            x += surf.get_width()

        return full_surf

    
    def render(self, screen):
        screen.blit(self.get_surf(), (self.x, self.y))
    
    def center_y(self, rect):
        self.y = rect.center[1]-self.get_height()/2

    def center_x(self, rect):
        self.x = rect.center[0]-self.get_width()/2
    
    def center(self, rect):
        self.center_x(rect)
        self.center_y(rect)

def get_text_size(string, size=30, font_name=None):
    if font_name is None:
        font_name = Text.default_font_name
    t = Text(0, 0, string, font_name, size)
    return t.get_width(), t.get_height()