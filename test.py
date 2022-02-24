import pygame
from chatapp.windowgui.text import Text
from chatapp.windowgui.window import Window
from chatapp.windowgui.util import Colors
pygame.init()

class MyWindow(Window):
    def __init__(self):
        super().__init__((500, 500))
        self.bg_color = Colors.WHITE
        self.t = Text(20, 50, "The best cure to cancer is eating five hundred mangos a day!", newline_width=200)
    
    def update(self):
        super().update()
        self.t.render(self.screen)


MyWindow().start()

