import pygame
from chatapp.windowgui.text import Text
from chatapp.windowgui.window import Window
from chatapp.windowgui.util import Colors, draw_border
pygame.init()

class MyWindow(Window):
    def __init__(self):
        super().__init__((500, 500))
        self.bg_color = Colors.WHITE
        self.t = Text(20, 50, "The best cure to cancer is eating five hundred mangos a day!",
        format={"color": (255, 0, 255)}, newline_width=200)
    
    def update(self):
        super().update()
        self.t.render(self.screen)
        draw_border(self.screen, pygame.Rect(40, 40, 100, 100), 1)




MyWindow().start()

