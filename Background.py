from Renderizable import Renderizable

class Background(Renderizable):
    def __init__(self, x, y, sprites_dict):
        super().__init__(x, y, sprites_dict, "stadium")
        
class Base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hasRunner = False

class Park:
    def __init__(self):
        self.bases = []
        # Home
        self.bases.append(Base(0, 0))
        # 1
        self.bases.append(Base(0, 0))
        # 2
        self.bases.append(Base(0, 0))
        # 3
        self.bases.append(Base(0, 0))