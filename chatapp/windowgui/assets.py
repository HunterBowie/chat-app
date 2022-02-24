import pygame
from os import path
from .util import Colors, load_img

def get_asset(type, name):
    if type == "fonts":
        return Assets.FONTS[name]
    if type == "sounds":
        pass

class Assets:
    CURRENT_DIR = path.dirname(__file__)
    IMAGES_DIR = path.join(CURRENT_DIR, "assets/images")
    SOUNDS_DIR = path.join(CURRENT_DIR, "assets/sounds")
    FOUNTS_DIR = path.join(CURRENT_DIR, "assets/fonts")

    FONTS = {
        "regular": pygame.font.get_default_font(),
        "rounded": path.join(FOUNTS_DIR, "rounded.ttf")
    }


    @classmethod
    def get_button_img(cls, pressed, scale, color_name):
        shape = "_square"
        if scale[0] > scale[1] * 1.50:
            shape = "_long"
        img_name = ""
        if pressed:
            img_name = color_name + "_button_down" + shape
        else:
            img_name = color_name + "_button_up" + shape
        img = load_img(img_name, cls.IMAGES_DIR)
        return pygame.transform.scale(img, scale)
    
    @classmethod
    def get_slider_img(cls):
        pass


    @classmethod
    def get_checkbox_img(cls):
        pass