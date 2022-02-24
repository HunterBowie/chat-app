import pygame
from os import path
from .windowgui.util import load_img
from .windowgui.assets import get_asset

class Assets:
    CURRENT_DIR = path.dirname(__file__)
    IMAGES_DIR = path.join(CURRENT_DIR, "assets/images")
    
    IMAGES = {
            "icon": load_img("icon", IMAGES_DIR, scale=(64, 64))
        }
    FONTS = {
        "rounded": get_asset("fonts", "rounded")
    }
    SOUNDS = {}


        