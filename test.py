from chatapp.windowgui.text import Text
from chatapp.windowgui.window import Window


class MyWindow(Window):
    def __init__(self):
        super().__init__((500, 500))
        t = Text(0, 0, "Hello")
    
    def update(self):
        super().update()
        self.t.render(self.screen)


MyWindow().start()
