import pygame
from Background import Background
import os

directory_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(directory_path)
BG_SPRITES = {"stadium" : pygame.image.load(os.path.join(directory_path,"stadium.jpg"))}

class Window:
    def __init__(self):
        pygame.display.set_caption("Baseball Game")
        self.background = Background(x=0, y=0, sprites_dict=BG_SPRITES)
        w = self.background.image.get_width()
        h = self.background.image.get_height()
        self.screen = pygame.display.set_mode((w, h))

    def render(self, renderList):
        for obj in renderList:
            obj.render(self.screen)
                       
    pass