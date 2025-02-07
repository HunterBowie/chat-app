import os

import pygame

from .assets import Assets
from .constants import Constants
from .ui import StartUI
from .windowgui.text import Text
from .windowgui.timers import RealTimer
from .windowgui.util import Colors
from .windowgui.window import Window


class App(Window):
    """Repersents the window for the app."""

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

        self.monitor = RealTimer()

    def update(self):
        self.monitor.reset()
        super().update()
        # print(f"cycle delay {time.monotonic()-self.monitor.start_time}")
