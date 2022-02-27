import pygame
from os import path
from .windowgui.util import load_img, Colors
from .windowgui.assets import get_asset, get_dir


class Assets:
    CURRENT_DIR = path.dirname(__file__)
    IMAGES_DIR = path.join(CURRENT_DIR, "assets/images")
    
    IMAGES = {
            "icon_small": load_img("icon", IMAGES_DIR, scale=(32, 32)),
            "icon_large": load_img("icon", IMAGES_DIR),
            "arrow_up": load_img("arrowUp", get_dir("images")),
            "arrow_left": load_img("arrowLeft", get_dir("images")),

        }
    FONTS = {
        "rounded": get_asset("fonts", "rounded")
    }
    SOUNDS = {}

    @classmethod
    def convert_imgs(cls):
        cls.IMAGES = {name: img.convert_alpha() for name,img in cls.IMAGES.items()}


        