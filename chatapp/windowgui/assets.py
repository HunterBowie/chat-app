import pygame
from os import path
from .util import Colors

# public
def load_img(img_name, img_path, ext=".png", colorkey=Colors.BLACK, scale=None):
    full_path = path.join(img_path, img_name) + ext
    try:
        img = pygame.image.load(full_path).convert()
    except FileNotFoundError:
        raise FileNotFoundError(f"no image for path {full_path}")
    if scale is not None:
        img = pygame.transform.scale(img, scale)
    img.set_colorkey(Colors.BLACK)
    return img

# private
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