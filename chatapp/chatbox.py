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
        chatsurf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        bg = chatsurf.copy()
        bg.fill(Colors.GREY)
        bg.set_alpha(100)
        chatsurf.blit(bg, (0, 0))

        y = self.rect.height-50
        for msg in self.messages:
            if msg["id"] == self.id:
                Text(100, y, msg["content"], newline_width=200).render(chatsurf)
            
            else:
                Text(0, y, msg["content"], newline_width=200).render(chatsurf)

            y -= Text(0, 0, "9").get_height()
        surface.blit(chatsurf, self.rect.topleft)

            
