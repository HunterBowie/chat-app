import pygame
from .windowgui.text import Text
from .windowgui.util import Colors

class ChatBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.messages = [] 
    
    def new_msg(self, msg):
        self.messages.insert(0, msg)
    
    def render(self, surface):
    
        box_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        bg = box_surf.copy()
        bg.fill(Colors.BLUE)
        bg.set_alpha(40)
        y = self.rect.height-30
        for msg in  self.messages:
            string = f"{msg['id']}: {msg['content']}"
            text = Text(0, y, string, size=25)
            text.render(box_surf)
            y -= 25
            if y < 0:
                break
        surface.blit(bg, self.rect.topleft)
        surface.blit(box_surf, self.rect.topleft)

            
