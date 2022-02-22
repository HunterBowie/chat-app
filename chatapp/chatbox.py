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
    
        for msg in self.messages:
            if msg["id"] == self.id:
                pass
            
            else:
                pass

            
