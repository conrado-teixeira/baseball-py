class Renderizable():
    def __init__(self, x, y, sprites_dict, initial_sprite):
        self.curr_sprite = initial_sprite
        self.sprites = {}
        for key,image in sprites_dict.items():
            self.sprites[key] = image
        self.set_image()
        self.x = x
        self.y = y

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def set_image(self):
        self.image = self.sprites[self.curr_sprite]