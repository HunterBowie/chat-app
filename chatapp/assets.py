import pygame
from os import path
from .windowgui.util import load_img
from .windowgui.assets import get_asset

class Assets:
    CURRENT_DIR = path.dirname(__file__)
    IMAGES_DIR = path.join(CURRENT_DIR, "assets/images")
    
    IMAGES = {
            "icon": load_img("icon", IMAGES_DIR, scale=(32, 32)),
            "icon_large": load_img("icon", IMAGES_DIR, scale=(32, 32))
        }
    FONTS = {
        "rounded": get_asset("fonts", "rounded")
    }
    SOUNDS = {}

    @classmethod
    def convert_imgs(cls):
        cls.IMAGES = {name: img.convert() for name,img in cls.IMAGES.items()}


        