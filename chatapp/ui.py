from .windowgui.ui import Button, TextBox
from .windowgui.util import root_rect, root_pos
from .windowgui.text import Text
from .constants import Constants
from .windowgui.ui import UIGroup
from .cmds import printCMD, ChangeUICMD

class JoinUI(UIGroup):
    def __init__(self, window):
        super().__init__(window)
        self.ui = {
        "join_textbox":  TextBox(printCMD, 0, -75, 200, 50)
        }
        root_rect(Constants.SCREEN_SIZE, self.ui["join_textbox"].rect, center_x=True, center_y=True)
    
        self.text = Text(0, 0, "Enter Host IP Adress")

        self.text.x, self.text.y = root_pos(
            Constants.SCREEN_SIZE, self.text.get_rect(), center_x=True, center_y=True)
    
    def update(self):
        super().update()
        self.text.render(self.window.screen)


class StartUI(UIGroup):
    def __init__(self, window):
        super().__init__(window)
        self.ui = {
        "join_button":  Button(printCMD, 0, 0, 175, 50, "white", top_img=Text(0, 0, "Join").get_surf()),
        "host_button":  Button(ChangeUICMD(window, JoinUI(window)), 0, -75, 175, 50, "white", top_img=Text(0, 0, "Host").get_surf()) 
        }

        root_rect(Constants.SCREEN_SIZE, self.ui["join_button"].rect, center_x=True, center_y=True)
        root_rect(Constants.SCREEN_SIZE, self.ui["host_button"].rect, center_x=True, center_y=True)
    
