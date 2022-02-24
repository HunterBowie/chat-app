from http.cookies import SimpleCookie
from lib2to3.pgen2.token import NEWLINE
import pygame
from .assets import Assets
from .util import Colors


def get_text_size(string, format):
    font = pygame.font.Font(format["font_file"], format["size"])
    surf = font.render(string, format["antialias"], format["color"])
    return surf.get_width(), surf.get_height()

class Text:
    default_format = {
        "font_file": pygame.font.get_default_font(),
        "size": 30,
        "antialias": True,
        "color": Colors.BLACK
    }

    def __init__(self, x, y, string, format=default_format, newline_width=None):
        self.format = format
        self.string = string
        self.x = x
        self.y = y
        self.newline_width = newline_width
        self.set(string)

    def set(self, string):
        self.lines = string.split("\n")
        self.string = string.replace("\n", "")
        if self.newline_width:
            new_lines = []
            
            for line in self.lines:
                new_line = "" 
                for char in line:
                    new_line = new_line + char
                    if get_text_size(new_line, self.format)[0] >= self.newline_width:
                        new_lines.append(new_line.strip())
                        new_line = ""
                    
                if new_line:
                    new_lines.append(new_line.strip())
            self.lines = new_lines
                    

    
    def add(self, string):
        self.set(self.string + string)
    
    def pop(self):
        char = self.string[len(self.string)-1]
        self.string = self.string[:len(self.string)-1]
        return char
    

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.get_width(), self.get_height())
    
    def get_surf(self):
        font = pygame.font.Font(self.format["font_file"], self.format["size"])

        if len(self.lines) > 1:
            renders = []    
            for string in self.lines:
                renders.append(font.render(string, self.format["antialias"], self.format["color"]))
            
            width = height = 0
            for line_surf in renders:
                width += line_surf.get_width()
                height += line_surf.get_height()
            
            surf = pygame.Surface((width, height), pygame.SRCALPHA)
            x = y = 0
            for line_surf in renders:
                surf.blit(line_surf, (x, y))
                y += line_surf.get_height()
            
        else:
            surf = font.render(self.string, self.format["antialias"], self.format["color"])
        
        return surf
        

    
    def render(self, screen):
        screen.blit(self.get_surf(), (self.x, self.y))
    
    def center_y(self, rect):
        self.y = rect.center[1]-self.get_height()/2

    def center_x(self, rect):
        self.x = rect.center[0]-self.get_width()/2
    
    def center(self, rect):
        self.center_x(rect)
        self.center_y(rect)



