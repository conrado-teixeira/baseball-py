# Content from Renderizable.py
import pygame

class Renderizable:
    def __init__(self, x, y, z, sprites_dict, initial_sprite, cast_shadow=True):
        self.hidden = False
        self.cast_shadow = cast_shadow
        self.curr_sprite = initial_sprite
        self.sprites = {}
        for key, image in sprites_dict.items():
            self.sprites[key] = image
        self.set_image()
        self.x = x
        self.y = y
        self.z = z
        self.shadow_color = (10, 10, 10)  # Shadow color
        self.shadow_offset = 10  # Adjust this value to control the shadow offset
        self.calculate_shadow_position()

    def render_shadow(self, screen):
        if self.cast_shadow:
            pygame.draw.circle(screen,self.shadow_color,(int(self.shadow_x), int(self.shadow_y)),5)

    def render(self, screen):
        if self.hidden:
            return
        # Render shadow first
        self.render_shadow(screen)
        # Render object on top of the shadow
        screen.blit(self.image, (self.x, self.y))

    def set_image(self):
        self.image = self.sprites[self.curr_sprite]

    def move(self):
        self.x += self.speed_vector[0]
        self.y += self.speed_vector[1]
        self.z += self.speed_vector[2]
        self.calculate_shadow_position()

    def calculate_shadow_position(self):
        if self.cast_shadow:
            # Calculate shadow size based on Z coordinate
            size_factor = max(1, 1 - self.z / 10)  # Adjust the factor as needed

            # Calculate shadow position based on Z coordinate
            self.shadow_x, self.shadow_y = self.image.get_rect().center
            self.shadow_y += self.shadow_offset * (self.z / 5)  # Adjust the factor as needed

            # Adjust the shadow size based on Z coordinate
            self.shadow_x = int(self.shadow_x * size_factor)
            self.shadow_y = int(self.shadow_y * size_factor)
