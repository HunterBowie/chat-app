import pygame
from .util import Textures

class UIElement:
    def __init__(self):
        pass

class Button(UIElement):
    def __init__(self, x, y, width, height, color_name, top_img=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.clicked = False
        self.active = False
        self.top_img = top_img
        self.top_img_x = self.top_img_y = 0
        if self.top_img:
            self.top_img_x = int(self.rect.width/2-self.top_img.get_width()/2)
            self.top_img_y = int(self.rect.height/2-self.top_img.get_height()/2)
            
        self._img_up = Textures.get(Textures.BUTTON_UP, (width, height), color_name)
        self._img_down = Textures.get(Textures.BUTTON_DOWN, (width, height-4), color_name)
    
    def update(self):
        self.active = False
        
    
    def eventloop(self, event):
        pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pos):
                self.clicked = True
                self.active = True


    def render(self, surface):
        pos = pygame.mouse.get_pos()
        if not pygame.mouse.get_pressed() == (1, 0, 0):
            self.clicked = False
                
        if self.clicked:
            surface.blit(self._img_down, self.rect.topleft)
        else:   
            surface.blit(self._img_up, (self.rect.left, self.rect.top-4))
        
        if self.top_img:
            if self.clicked:
                surface.blit(self.top_img, (self.top_img_x+self.rect.x, self.top_img_y+self.rect.y))
            else:
                surface.blit(self.top_img, (self.top_img_x+self.rect.x, self.top_img_y+self.rect.y-4))


class Slider(UIElement):
    pass

class TextBox(UIElement):
    pass

