import pygame, pyperclip
from .util import Textures, Colors
from .text import Text, get_text_size
from .constants import Constants
from .timers import RealTimer

class UIEvent:
    BUTTON_CLICK = pygame.USEREVENT 
    TEXTBOX_POST = pygame.USEREVENT + 1






class UIElement:
    def __init__(self, id, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.id = id

    def post_event(self, event_type):
        event_data = {
            "ui_element": self,
            "ui_id": self.id,
        }
        pygame.event.post(pygame.event.Event(event_type, event_data))
                

class Button(UIElement):
    def __init__(self, id, x, y, width, height, color_name="white", top_img=None):
        super().__init__(id, x, y, width, height)
        self.clicked = False
        self.top_img = top_img
        self.top_img_x = self.top_img_y = 0
        if self.top_img:
            self.top_img_x = int(self.rect.width/2-self.top_img.get_width()/2)
            self.top_img_y = int(self.rect.height/2-self.top_img.get_height()/2)
            
        self._img_up = Textures.get(Textures.BUTTON_UP, (width, height), color_name)
        self._img_down = Textures.get(Textures.BUTTON_DOWN, (width, height-4), color_name)
    
    def eventloop(self, event):
        pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pos):
                self.clicked = True
                self.post_event(UIEvent.BUTTON_CLICK) 
    
    def update(self):
        pos = pygame.mouse.get_pos()
        if not pygame.mouse.get_pressed() == (1, 0, 0):
            self.clicked = False
                
        

    def render(self, surface):
        
        if self.clicked:
            surface.blit(self._img_down, self.rect.topleft)
        else:   
            surface.blit(self._img_up, (self.rect.left, self.rect.top-4))
        
        if self.top_img:
            if self.clicked:
                surface.blit(self.top_img, (self.top_img_x+self.rect.x, self.top_img_y+self.rect.y))
            else:
                surface.blit(self.top_img, (self.top_img_x+self.rect.x, self.top_img_y+self.rect.y-4))


class Slider(UIElement):
    pass

class TextBox(UIElement):
    def __init__(self, id, x, y, width, height, font_size=25, border=True):
        super().__init__(id, x, y, width, height)
        self.text = Text(0, 0, "", size=font_size)
        
        self.border = border
        self.selected = False
        self.cursor_blink = True
        self.cursor_timer = RealTimer()
        self.cursor_timer.start()
        self.backspace_count = 0


    def is_appendable(self, string):
        text_size = get_text_size(self.text.string + string, size=self.text.size)
        if text_size[0] >= (self.rect.width-Constants.TEXTBOX_MARGIN*2):
            return False
        return True
    

    def eventloop(self, event):
        keys = pygame.key.get_pressed()
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pos):
                self.selected = True
            else:
                self.selected = False

        if self.selected:
            if event.type == pygame.KEYDOWN:
                hit_key = True
                key_name = pygame.key.name(event.key)
                if key_name == "space":
                    if self.is_appendable(" "):
                        self.text.add(" ")
                elif key_name == "backspace":
                    if self.text.string:
                        self.text.pop()
                elif key_name == "return":
                    self.post_event(UIEvent.TEXTBOX_POST)

                elif len(key_name) == 1:
                    string_data = key_name
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        string_data = key_name.upper()
                        if key_name in Constants.TEXTBOX_SHIFT_CHARS.keys():
                            string_data = Constants.TEXTBOX_SHIFT_CHARS[key_name]
                        elif key_name == "v" and event.mod and pygame.KMOD_CTRL:
                            if self.is_appendable(pyperclip.paste()):
                                string_data = pyperclip.paste()
                    if self.is_appendable(string_data):
                        self.text.add(string_data)
                else:
                    hit_key = False
                
                if hit_key:
                    self.cursor_timer.reset()
                    self.cursor_blink = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    self.backspace_count = 0
    
    def update(self):
        self.text.center_y(pygame.Rect(0, 0, self.rect.width, self.rect.height))
        keys = pygame.key.get_pressed()
        if self.selected:
            if keys[pygame.K_BACKSPACE]:
                self.backspace_count += 1
                if self.backspace_count == Constants.TEXTBOX_BACKSPACE_SPEED:
                    self.backspace_count = 0
                    if self.text.string:
                        self.text.pop()
                
        
    def render(self, surface):
        width = Constants.TEXTBOX_BORDER_WIDTH
        white_rect = pygame.Rect(int(self.rect.x+width/2), int(self.rect.y+width/2), self.rect.width-width, self.rect.height-width)
        pygame.draw.rect(surface, Colors.BLACK, self.rect)
        pygame.draw.rect(surface, Colors.WHITE, white_rect)
        surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.text.render(surf)
        surface.blit(surf, (self.rect.x + Constants.TEXTBOX_MARGIN, self.rect.y))


        
        
        
        # render cursor
        if self.selected:
            x = self.rect.x+Constants.TEXTBOX_MARGIN+self.text.get_width()
            string = ""
            if self.cursor_blink:
                string = "|"
            
            if self.cursor_timer.passed(Constants.TEXTBOX_CURSOR_BLINK_TIME):
                self.cursor_timer.reset()
                self.cursor_blink = not self.cursor_blink
            

            text = Text(x, 0, string)
            text.center_y(self.rect)
            text.render(surface)



class UIManager:
    def __init__(self, window):
        self.window = window
        self.ui = []
    
    def stop(self):
        pass
    
    def get_element(self, id):
        for element in self.ui:
            if element.id == id:
                return element
        raise ValueError(f"no element with id: {id}")

    def eventloop(self, event):
        for element in self.ui:
            element.eventloop(event)
    
    def update(self):
        for element in self.ui:
            element.update()
            element.render(self.window.screen)


