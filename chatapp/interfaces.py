from .windowgui.ui import Button
from .windowgui.util import root_pos
from .windowgui.text import Text
from .constants import Constants

START_UI = {
    "join":  Button(0, 0, 175, 50, "white", top_img=Text(0, 0, "Join").get_surf()),
    "host":  Button(0, -75, 175, 50, "white", top_img=Text(0, 0, "Host").get_surf()) 
}

root_pos(Constants.SCREEN_SIZE, START_UI["join"].rect, center_x=True, center_y=True)
root_pos(Constants.SCREEN_SIZE, START_UI["host"].rect, center_x=True, center_y=True)