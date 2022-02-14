import pygame
from .windowgui.window import Window
from .windowgui.util import Colors, root_pos, ROUNDED_FONT
from .windowgui.text import Text
from .constants import Constants
from .windowgui.ui import Button
from .interfaces import START_UI


class App(Window):
    def __init__(self):
        super().__init__(Constants.SCREEN_SIZE)
        self.bg_color = Colors.WHITE
        pygame.display.set_caption("Chat App")
        Text.FONT = ROUNDED_FONT
        self.ui = START_UI
    
    def input_handler(self, id):
        if id == "host_button":
            print("hosting")
    
    def update(self):
        super().update()
    