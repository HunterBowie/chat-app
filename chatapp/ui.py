import pygame, random, threading
from .windowgui.ui import Button, TextBox
from .windowgui.util import root_rect, Flash, Colors
from .windowgui.text import Text
from .constants import Constants
from .windowgui.ui import UIManager, UIEvent
from .chatbox import ChatBox
from .chatconn import ChatConn
from .util import ConnIDTaken, ConnInvalidIP, ConnPortTaken, ConnRefused
from .assets import Assets

class ChatUI(UIManager):
    def __init__(self, window, chatconn):
        super().__init__(window)
        self.chatbox = ChatBox(25, 60, Constants.SCREEN_WIDTH-50, 310, chatconn.id)
        self.chatconn = chatconn

        self.ui = [
            TextBox("send_box", 0, 150, 300, 50),
            Button("back_btn", 10, 0, 50, 50, top_img=Assets.IMAGES["arrow_left"], hide_button=True)

        ]
        root_rect(Constants.SCREEN_SIZE, self.get_element("back_btn").rect, bottom_y=True)

        
        root_rect(
            Constants.SCREEN_SIZE, self.get_element("send_box").rect,
            center_x=True, center_y=True
        )

        self.info_text = Text(0, -75, "")
        self.ip_text = Text(0, -35, "")
        self.id_text = Text(0, 10, chatconn.id)
        self.conn_text = Text(0, 0, "")
        self.conn_text_value = None
        self.conn_text_num = 0

        self.conn_text.x, self.conn_text.y = root_rect(Constants.SCREEN_SIZE, self.conn_text.get_rect(),
        center_x=True, bottom_y=True
        )
    
        self.id_text.x, self.id_text.y = root_rect(Constants.SCREEN_SIZE, self.id_text.get_rect(),
        top_y=True, center_x=True)
        
        if self.chatconn.type == "server":
            self.info_text.set("Server")
            if Constants.HAS_INTERNET:
                self.ip_text.set(ChatConn.IP_PRIVATE)
            else:
                self.ip_text.set("NONE")
        else:
            self.info_text.set("Client")
            if Constants.HAS_INTERNET:
                self.ip_text.set(self.chatconn.addr[0])
            else:
                self.ip_text.set("NONE")
        
        
        self.info_text.x, self.info_text.y = root_rect(
            Constants.SCREEN_SIZE, self.info_text.get_rect(),
            center_x=True, bottom_y=True
        )
        self.ip_text.x, self.ip_text.y = root_rect(
            Constants.SCREEN_SIZE, self.ip_text.get_rect(),
            center_x=True, bottom_y=True
        )
    
    def update_info_text(self):
        
            if self.conn_text_value:
                self.conn_text.format["color"] = Colors.GREEN
                if self.chatconn.type == "server":
                    self.conn_text.set(f"Clients: {len(self.chatconn.connections)}")
                else:
                    self.conn_text.set("Connected")
                
            else:
                self.conn_text.format["color"] = Colors.RED
                if self.chatconn.type == "server":
                    self.conn_text.set("No Clients")
                else:
                    self.conn_text.set("Not Connected")
                
            self.conn_text.x = self.conn_text.y = 0
            self.conn_text.x, self.conn_text.y = root_rect(Constants.SCREEN_SIZE, self.conn_text.get_rect(),
            center_x=True, bottom_y=True
            )

    def update(self):
        super().update()
        while(self.chatconn.has_msg()):
            msg = self.chatconn.get_msg()
            self.chatbox.new_msg(msg)
        
        connected = False
        if self.chatconn.connections:
            connected = True
        
        if connected != self.conn_text_value:
            # Client: Connected Disconnected
            # Server: No Clients, # Clients 
            self.conn_text_value = connected
            self.update_info_text()
        
        if self.conn_text_num != len(self.chatconn.connections):
            self.conn_text_num = len(self.chatconn.connections)
            self.update_info_text
            
            
        self.chatbox.render(self.window.screen)
        self.info_text.render(self.window.screen)
        self.ip_text.render(self.window.screen)
        self.id_text.render(self.window.screen)
        self.conn_text.render(self.window.screen)

    def eventloop(self, event):
        super().eventloop(event)
        if event.type == pygame.MOUSEWHEEL:
            self.chatbox.scroll += event.y*10

        if event.type == UIEvent.BUTTON_CLICK:
            if event.ui_id == "back_btn":
                self.chatconn.running = False
                while threading.active_count() > 1:
                    print("waiting")
                self.window.ui_manager = ConnectUI(self.window, self.chatconn.id)

        if event.type == UIEvent.TEXTBOX_POST:
            data = event.ui_element.text.string
            if data.strip() != "":

                event.ui_element.text.set("")
                self.chatconn.send_msg(data)
                self.chatbox.new_msg({"id":self.chatconn.id, "content": data})

    def stop(self):
        self.chatconn.running = False
  


class JoinUI(UIManager):
    def __init__(self, window, id):
        super().__init__(window)
        self.ui = [
            TextBox("ip_box", 0, 0, 190, 50),
            Button("back_btn", 10, 0, 50, 50, top_img=Assets.IMAGES["arrow_left"], hide_button=True)

        ]
        root_rect(Constants.SCREEN_SIZE, self.get_element("back_btn").rect, bottom_y=True)

        self.ip_text = Text(0, -100, "Enter Server IP Address")
        self.id = id
        root_rect(Constants.SCREEN_SIZE, self.get_element("ip_box").rect, center_x=True, center_y=True)
        self.ip_text.x, self.ip_text.y = root_rect(Constants.SCREEN_SIZE, self.ip_text.get_rect(), center_x=True, center_y=True)
    
    def eventloop(self, event):
        super().eventloop(event)

        if event.type == UIEvent.BUTTON_CLICK:
            if event.ui_id == "back_btn":
                self.stop()
                self.window.ui_manager = ConnectUI(self.window, self.id)
      
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
        Button("join_btn", 0, 0, 175, 50, "white", top_img=Text(0, 0, "Join").surface),
        Button("host_btn", 0, -75, 175, 50, "white", top_img=Text(0, 0, "Host").surface),
        Button("back_btn", 10, 0, 50, 50, top_img=Assets.IMAGES["arrow_left"], hide_button=True)
        ]

        self.id = id
        root_rect(Constants.SCREEN_SIZE, self.get_element("back_btn").rect, bottom_y=True)
        root_rect(Constants.SCREEN_SIZE, self.get_element("join_btn").rect, center_x=True, center_y=True)
        root_rect(Constants.SCREEN_SIZE, self.get_element("host_btn").rect, center_x=True, center_y=True)
    
    def eventloop(self, event):
        super().eventloop(event)

        if event.type == UIEvent.BUTTON_CLICK:
            if event.ui_id == "back_btn":
                self.window.ui_manager = StartUI(self.window)
            if event.ui_id == "join_btn":
                self.window.ui_manager = JoinUI(self.window, self.id)
            elif event.ui_id == "host_btn":
                try:
                    ui_manager = ChatUI(self.window, ChatConn("server", ChatConn.IP_PRIVATE, self.id))
                except ConnPortTaken:
                    flash = Flash(0, 0, Text(0, 0, "cannot host two servers \n on same computer", {"size": 20}),
                     (240, 50), Colors.LIGHT_YELLOW)
                    flash.x, flash.y = root_rect(Constants.SCREEN_SIZE, flash.surface.get_rect(),
                    center_x=True, top_y=True)
                    self.window.flash(flash)
                else:
                    self.window.ui_manager = ui_manager

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
                if id.strip() == "":
                    flash = Flash(0, 0, Text(0, 0, "enter a valid username", {"size": 20}),
                     (240, 50), Colors.LIGHT_YELLOW)
                    flash.x, flash.y = root_rect(Constants.SCREEN_SIZE, flash.surface.get_rect(),
                    center_x=True, top_y=True)
                    self.window.flash(flash)
                else:
                    if id.strip() == "f":
                        flash = Flash(0, 0, Text(0, 0, "nice username!", {"size": 20}),
                        (240, 50), Colors.LIGHT_GREEN)
                        flash.x, flash.y = root_rect(Constants.SCREEN_SIZE, flash.surface.get_rect(),
                        center_x=True, top_y=True)
                        self.window.flash(flash)
                    self.window.ui_manager = ConnectUI(self.window, id)
                
                
    
    def update(self):
        super().update()
        self.prompt_text.render(self.window.screen)
