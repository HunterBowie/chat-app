from .windowgui.ui import Button, TextBox
from .windowgui.util import root_rect, root_pos
from .windowgui.text import Text
from .constants import Constants
from .windowgui.ui import UIManager
from .chatbox import ChatBox
from .socket import Client, Server

class StartUI(UIManager):
    def __init__(self, window):
        super().__init__(window)
        self.ui = [
        Button("join_btn", 0, 0, 175, 50, "white", top_img=Text(0, 0, "Join").get_surf()),
        Button("host_btn", 0, -75, 175, 50, "white", top_img=Text(0, 0, "Host").get_surf()) 
        ]

        root_rect(Constants.SCREEN_SIZE, self.ui["join_button"].rect, center_x=True, center_y=True)
        root_rect(Constants.SCREEN_SIZE, self.ui["host_button"].rect, center_x=True, center_y=True)
    
    def update(self):
        pass