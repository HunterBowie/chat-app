import pygame
from .windowgui.window import Window
from .windowgui.util import Colors, root_pos, ROUNDED_FONT
from .windowgui.text import Text
from .constants import Constants
from .windowgui.ui import Button
from .ui import StartUI


class App(Window):
    def __init__(self):
        super().__init__(Constants.SCREEN_SIZE)
        pygame.display.set_caption("Chat App")
        Text.FONT = ROUNDED_FONT
        self.bg_color = Colors.WHITE

        self.ui_group = StartUI(self)

    
    def update(self):

        super().update()
    