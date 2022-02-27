from email import message
import pygame
from .windowgui.text import Text, get_text_size, render_text_background
from .windowgui.util import Colors, get_surf, render_border

class ChatBox:
    def __init__(self, x, y, width, height, id):
        self.rect = pygame.Rect(x, y, width, height)
        self.messages = []
        self.id = id
        self.scroll = 0
    
    def new_msg(self, msg):
        self.scroll = 0
        self.messages.insert(0, msg)
    
    def render(self, surface):
        chatsurf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        chatsurf.blit(get_surf(self.rect.size, Colors.GREY, 100), (0, 0))

        render_border(surface, self.rect, 3)
        
        if self.messages:
            text_width = 150
            margin = 10
            y = self.rect.height + self.scroll
            x = 0
            color = None
            for msg in self.messages:
                if y < 0:
                    break
                
                text = Text(0, 0, msg["content"], {"size": 20}, newline_width=text_width)
                y -= text.get_height()+margin*2
                
                if y > self.rect.height:
                    continue   
                
                if msg["id"] == self.id:
                    x = self.rect.width-text.get_width()-margin
                    color = Colors.GREEN
                else:
                    x = margin
                    color = Colors.RED
                text.x, text.y = x, y
                render_text_background(chatsurf, text, color, 75, 10)
                text.render(chatsurf)
                
        surface.blit(chatsurf, self.rect.topleft)

            
