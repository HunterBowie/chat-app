import pygame, os
from .windowgui.window import Window
from .windowgui.util import Colors
from .windowgui.text import Text
from .constants import Constants
from .ui import StartUI
from .assets import Assets


class App(Window):
    def __init__(self):
        super().__init__(Constants.SCREEN_SIZE)
        Assets.convert_imgs()
        pygame.display.set_caption("Chat App")
        if os.name == Constants.WIN_OS_NAME:
            pygame.display.set_icon(Assets.IMAGES["icon_small"])
        else:
            pygame.display.set_icon(Assets.IMAGES["icon_large"])
        Text.default_format["font_file"] = Assets.FONTS["rounded"]
        self.bg_color = Colors.WHITE

        self.ui_manager = StartUI(self)

    