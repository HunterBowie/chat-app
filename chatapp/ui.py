import pygame, random
from .windowgui.ui import Button, TextBox
from .windowgui.util import root_rect, Flash, Colors
from .windowgui.text import Text
from .constants import Constants
from .windowgui.ui import UIManager, UIEvent
from .chatbox import ChatBox
from .chatconn import ChatConn
from .util import ConnIDTaken, ConnInvalidIP, ConnRefused

class ChatUI(UIManager):
    def __init__(self, window, chatconn):
        super().__init__(window)
        self.chatbox = ChatBox(25, 60, Constants.SCREEN_WIDTH-50, 310, chatconn.id)
        self.chatconn = chatconn

        self.ui = [
            TextBox("send_box", 0, 150, 300, 50)
        ]
        
        root_rect(
            Constants.SCREEN_SIZE, self.get_element("send_box").rect,
            center_x=True, center_y=True
        )

        self.info_text = Text(0, -35, "")
        self.ip_text = Text(0, 0, "")
        self.id_text = Text(0, 10, chatconn.id)
    
        self.id_text.x, self.id_text.y = root_rect(Constants.SCREEN_SIZE, self.id_text.get_rect(),
        top_y=True, center_x=True)
        
        if self.chatconn.type == "server":
            self.info_text.string = "Server"
            self.ip_text.string = ChatConn.IP_PRIVATE
        else:
            self.info_text.string = "Client"
            self.ip_text.string = self.chatconn.addr[0]
        
        
        self.info_text.x, self.info_text.y = root_rect(
            Constants.SCREEN_SIZE, self.info_text.get_rect(),
            center_x=True, bottom_y=True
        )
        self.ip_text.x, self.ip_text.y = root_rect(
            Constants.SCREEN_SIZE, self.ip_text.get_rect(),
            center_x=True, bottom_y=True
        )

    def update(self):
        super().update()
        for i in range(len(self.chatconn.in_queue)):
            msg = self.chatconn.in_queue.pop(0)
            self.chatbox.new_msg(msg)

        self.chatbox.render(self.window.screen)
        self.info_text.render(self.window.screen)
        self.ip_text.render(self.window.screen)
        self.id_text.render(self.window.screen)

    def eventloop(self, event):
        super().eventloop(event)
        if event.type == pygame.MOUSEWHEEL:
            self.chatbox.scroll += event.y*2

        if event.type == UIEvent.TEXTBOX_POST:
            data = event.ui_element.text.string
            event.ui_element.text.set("")
            self.chatconn.out_queue.append(data)
            self.chatbox.new_msg({"id":self.chatconn.id, "content": data})

    def stop(self):
        self.chatconn.running = False
  


class JoinUI(UIManager):
    def __init__(self, window, id):
        super().__init__(window)
        self.ui = [
        TextBox("ip_box", 0, 0, 190, 50),
        ]
        self.ip_text = Text(0, -100, "Enter Server IP Address")
        self.id = id
        root_rect(Constants.SCREEN_SIZE, self.get_element("ip_box").rect, center_x=True, center_y=True)
        self.ip_text.x, self.ip_text.y = root_rect(Constants.SCREEN_SIZE, self.ip_text.get_rect(), center_x=True, center_y=True)
    
    def eventloop(self, event):
        super().eventloop(event)

      
        if event.type == UIEvent.TEXTBOX_POST:
            if event.ui_id == "ip_box": 
                ip = event.ui_element.text.string
                try:
                    chatconn = ChatConn("client", ip, self.id)
                    
                except ConnIDTaken:
                    flash = Flash(0, 0, Text(0, 0, "username taken", {"size": 20}),
                     (240, 50), Colors.LIGHT_YELLOW)
                    flash.x, flash.y = root_rect(Constants.SCREEN_SIZE, flash.surface.get_rect(),
                    center_x=True, top_y=True)
                    self.window.flash(flash)
                
                except ConnInvalidIP:
                    flash = Flash(0, 0, Text(0, 0, "invalid IP address", {"size": 20}),
                     (240, 50), Colors.LIGHT_YELLOW)
                    flash.x, flash.y = root_rect(Constants.SCREEN_SIZE, flash.surface.get_rect(),
                    center_x=True, top_y=True)
                    self.window.flash(flash)
                
                except ConnRefused:
                    flash = Flash(0, 0, Text(0, 0, "failed to join server", {"size": 20}),
                     (240, 50), Colors.LIGHT_YELLOW)
                    flash.x, flash.y = root_rect(Constants.SCREEN_SIZE, flash.surface.get_rect(),
                    center_x=True, top_y=True)
                    self.window.flash(flash)
                
                else:
                    self.window.ui_manager = ChatUI(self.window, chatconn)

                
                
    
    def update(self):
        super().update()
        self.ip_text.render(self.window.screen)


class ConnectUI(UIManager):
    def __init__(self, window, id):
        super().__init__(window)
        self.ui = [
        Button("join_btn", 0, 0, 175, 50, "white", top_img=Text(0, 0, "Join").get_surf()),
        Button("host_btn", 0, -75, 175, 50, "white", top_img=Text(0, 0, "Host").get_surf()) 
        ]
        self.id = id

        root_rect(Constants.SCREEN_SIZE, self.get_element("join_btn").rect, center_x=True, center_y=True)
        root_rect(Constants.SCREEN_SIZE, self.get_element("host_btn").rect, center_x=True, center_y=True)
    
    def eventloop(self, event):
        super().eventloop(event)

        if event.type == UIEvent.BUTTON_CLICK:
            if event.ui_id == "join_btn":
                self.window.ui_manager = JoinUI(self.window, self.id)
            elif event.ui_id == "host_btn":
                self.window.ui_manager = ChatUI(self.window, ChatConn("server", ChatConn.IP_PRIVATE, self.id))

class StartUI(UIManager):
    def __init__(self, window):
        super().__init__(window)
        self.ui = [
            TextBox("id_box", 0, 0, 190, 50)
        ]

        self.prompt_text = Text(0, -100, "Enter Your Username")

        root_rect(Constants.SCREEN_SIZE, self.get_element("id_box").rect, 
        center_x=True, center_y=True)

        self.prompt_text.x, self.prompt_text.y = root_rect(Constants.SCREEN_SIZE, self.prompt_text.get_rect(), 
        center_x=True, center_y=True)
    
    def eventloop(self, event):
        super().eventloop(event)

        if event.type == UIEvent.TEXTBOX_POST:
            if event.ui_id == "id_box":
                id = event.ui_element.text.string
                self.window.ui_manager = ConnectUI(self.window, id)
                
                
    
    def update(self):
        super().update()
        self.prompt_text.render(self.window.screen)
