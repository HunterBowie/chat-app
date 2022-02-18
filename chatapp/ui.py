import pygame
from .windowgui.ui import Button, TextBox
from .windowgui.util import root_rect, root_pos
from .windowgui.text import Text
from .constants import Constants
from .windowgui.ui import UIManager, UIEvent
from .chatbox import ChatBox
from .socket import Client, Server


class JoinSocketUI(UIManager):
    def __init__(self, window):
        super().__init__(window)
        self.ui = [
        TextBox("ip_txtbox", 0, -100, 175, 50),
        ]
        self.ip_text = Text(0, 0, "Enter Host IP Address")

        root_rect(Constants.SCREEN_SIZE, self.get_element("ip_txtbox").rect, center_x=True, center_y=True)
        self.ip_text.x, self.ip_text.y = root_pos(Constants.SCREEN_SIZE, self.ip_text.get_rect(), center_x=True, center_y=True)
    
    def eventloop(self, event):
        super().eventloop(event)

        if event.type == UIEvent.TEXTBOX_POST:
            if event.ui_id == "ip_txtbox":
                print("got ip and sendingit")
    
    def update(self):
        super().update()
        self.ip_text.render(self.window.screen)


class StartUI(UIManager):
    def __init__(self, window):
        super().__init__(window)
        self.ui = [
        Button("join_btn", 0, 0, 175, 50, "white", top_img=Text(0, 0, "Join").get_surf()),
        Button("host_btn", 0, -75, 175, 50, "white", top_img=Text(0, 0, "Host").get_surf()) 
        ]

        root_rect(Constants.SCREEN_SIZE, self.get_element("join_btn").rect, center_x=True, center_y=True)
        root_rect(Constants.SCREEN_SIZE, self.get_element("host_btn").rect, center_x=True, center_y=True)
    
    def eventloop(self, event):
        super().eventloop(event)

        if event.type == UIEvent.BUTTON_CLICK:
            if event.ui_id == "join_btn":
                self.window.ui_manager = JoinSocketUI(self.window)
            elif event.ui_id == "host_btn":
                print("hosting")