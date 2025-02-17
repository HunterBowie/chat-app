from http.cookies import SimpleCookie
from lib2to3.pgen2.token import NEWLINE
from tarfile import DEFAULT_FORMAT
import pygame
from .assets import Assets
from .util import Colors, get_surf


class Text:
    default_format = {
        "font_file": pygame.font.get_default_font(),
        "size": 30,
        "antialias": True,
        "color": Colors.BLACK
    }

    def __init__(self, x, y, string, format=None, newline_width=None):
        self.format = format
        if self.format is None:
            self.format = self.default_format.copy()
        for setting, value in self.default_format.items():
            if setting not in self.format:
                self.format[setting] = value
        self.x = x
        self.y = y
        self.newline_width = newline_width
        self.set(string)

    def set(self, string):
        self.raw_string = string
        self.lines = string.split("\n")
        self.string = string.replace("\n", "")
        if self.newline_width:
            new_lines = []
            for line in self.lines:
                new_line = "" 
                for char in line:
                    new_line = new_line + char
                    if get_text_size(new_line, self.format)[0] >= self.newline_width and char == " ":
                        new_lines.append(new_line.strip())
                        new_line = ""
                if new_line:
                    new_lines.append(new_line.strip())
            self.lines = new_lines
        self._load_surf()
    
    def add(self, string):
        self.set(self.raw_string + string)
    
    def pop(self):
        char = self.string[len(self.string)-1]
        self.set(self.string[:len(self.string)-1])
        return char
    
    def get_width(self):
        return self.surface.get_width()
    
    def get_height(self):
        return self.surface.get_height()
    
    def get_size(self):
        return self.get_width(), self.get_height()

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.get_width(), self.get_height())
    
    def _load_surf(self):
        font = pygame.font.Font(self.format["font_file"], self.format["size"])

        if len(self.lines) > 1:
            renders = []    
            for string in self.lines:
                renders.append(font.render(string, self.format["antialias"], self.format["color"]))
            
            height = 0
            width = 0
            for line_surf in renders:
                height += line_surf.get_height()
                if line_surf.get_width() > width:
                    width = line_surf.get_width()
            
            self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
            x = y = 0
            for line_surf in renders:
                self.surface.blit(line_surf, (x, y))
                y += line_surf.get_height()
            
        else:
            self.surface = font.render(self.string, self.format["antialias"], self.format["color"])
    

    
    def render(self, screen):
        screen.blit(self.surface, (self.x, self.y))
    
    def center_y(self, rect):
        self.y = rect.center[1]-self.get_height()/2

    def center_x(self, rect):
        self.x = rect.center[0]-self.get_width()/2
    
    def center(self, rect):
        self.center_x(rect)
        self.center_y(rect)




def render_text_background(surface, text, color, alpha, margin):
    surf = get_surf((text.get_width()+margin, text.get_height()+margin), color, alpha)
    surface.blit(surf, (int(text.x-margin/2), int(text.y-margin/2)))

def get_text_size(string, format=Text.default_format):
    if format != Text.default_format:
        for setting, value in Text.default_format.items():
            if setting not in format:
                format[setting] = value
    font = pygame.font.Font(format["font_file"], format["size"])
    surf = font.render(string, format["antialias"], format["color"])
    return surf.get_width(), surf.get_height()