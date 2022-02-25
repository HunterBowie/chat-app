import pygame
from .windowgui.text import Text, get_text_size
from .windowgui.util import Colors

class ChatBox:
    def __init__(self, x, y, width, height, id):
        self.rect = pygame.Rect(x, y, width, height)
        self.messages = [] 
        self.id = id
    
    def new_msg(self, msg):
        self.messages.insert(0, msg)
    
    def _render_msg(self, msg, x, y, color):
        string = msg["content"]
         

    def render(self, surface):
        bg = pygame.Surface(self.rect.size)
        bg.fill(Colors.GREY)
        bg.set_alpha(100)
        surface.blit(bg, self.rect.topleft)
        x, y = self.rect.x, self.rect.y
        for msg in self.messages:
            if msg["id"] == self.id:
                Text(x, y, msg["content"]).render(surface)
            
            else:
                Text(x, y, msg["content"]).render(surface)

            y += Text(0, 0, "9").get_height()

            
