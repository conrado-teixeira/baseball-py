import pygame
from Background import Background

BG_SPRITES = {"stadium" : pygame.image.load("stadium.jpg")}

class Window:
    def __init__(self):
        pygame.display.set_caption("Baseball Game")
        self.background = Background(x=0, y=0, sprites_dict=BG_SPRITES)
        w = self.background.image.get_width()
        h = self.background.image.get_height()
        self.screen = pygame.display.set_mode((w, h))

    def render(self, gameObjects):
        self.background.render(self.screen)
        for obj in gameObjects:
            obj.render(self.screen)
                       
    pass