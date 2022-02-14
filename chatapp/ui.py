from .windowgui.ui import Button
from .windowgui.util import root_pos
from .windowgui.text import Text
from .constants import Constants
from .windowgui.ui import UIGroup

class TestUI(UIGroup)


class StartUI(UIGroup):
    def __init__(self, window):
        super().__init__(window)
        self.ui = {
        "join_button":  Button(0, 0, 175, 50, "white", top_img=Text(0, 0, "Join").get_surf()),
        "host_button":  Button(0, -75, 175, 50, "white", top_img=Text(0, 0, "Host").get_surf()) 
        }

        root_pos(Constants.SCREEN_SIZE, self.ui["join_button"].rect, center_x=True, center_y=True)
        root_pos(Constants.SCREEN_SIZE, self.ui["host_button"].rect, center_x=True, center_y=True)
    
    def handler_input(self, id):
        if id == "host_button":
            self.window.ui_group = 
