
class ChangeUICMD:
    def __init__(self, window, ui_group):
        self.window = window
        self.ui_group = ui_group
    
    def __call__(self):
        self.window.ui_group = self.ui_group


def printCMD():
    print("testing functions")
