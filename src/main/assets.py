from os import pardir, path

import pygame

from .windowgui.assets import get_asset, get_dir
from .windowgui.util import Colors, load_img


class Assets:
    """Repersents loaded assets."""
    CURRENT_DIR = path.dirname(__file__)
    PROJECT_DIR = path.abspath(path.join(CURRENT_DIR, pardir, pardir))
    IMAGES_DIR = path.join(PROJECT_DIR, "assets/images")

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
        cls.IMAGES = {name: img.convert_alpha()
                      for name, img in cls.IMAGES.items()}
