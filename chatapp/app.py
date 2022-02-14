import pygame
from .windowgui.window import Window
from .windowgui.util import Colors, root_pos, ROUNDED_FONT
from .windowgui.text import Text
from .constants import Constants
from .windowgui.ui import Button
from .interfaces import START_UI


class App:
    def __init__(self):
        self.window = Window(Constants.SCREEN_SIZE)
        self.window.bg_color = Colors.WHITE
        pygame.display.set_caption("Chat App")
        Text.FONT = ROUNDED_FONT

        self.window.ui = START_UI

        

    def start(self):
        self.window.start()