import pygame
from os import path
from .windowgui.assets import load_img

class Assets:
    CURRENT_DIR = path.dirname(__file__)
    IMAGES_DIR = path.join(CURRENT_DIR, "assets/images")
    
    IMAGES = {}
    FONTS = {}
    SOUNDS = {}


    @classmethod
    def init(cls):
        cls.IMAGES = {
            "icon": load_img("icon", cls.IMAGES_DIR, scale=(64, 64))
        }
        