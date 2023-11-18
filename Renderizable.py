# Content from Renderizable.py
import pygame

class Renderizable:
    def __init__(self, x, y, z, sprites_dict, initial_sprite):
        self.hidden = False
        self.draw_shadow = False
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

    def render(self, screen):
        if not self.hidden:
            # Render shadow first
            if self.draw_shadow:
                pygame.draw.circle(screen, self.shadow_color, (int(self.shadow_x), int(self.shadow_y)), self.image.get_rect().width)

            # Render object on top of the shadow
            screen.blit(self.image, (self.x, self.y))

    def set_image(self):
        self.image = self.sprites[self.curr_sprite]

    def move(self):
        pass  # Placeholder for movement, override in subclasses

    def calculate_shadow_position(self):
        # Calculate shadow position based on Z coordinate
        self.shadow_x, self.shadow_y = self.image.get_rect().center
        self.shadow_y += self.shadow_offset * (self.z / 5)  # Adjust the factor as needed

    def adjust_z(self, delta_z):
        self.z += delta_z
        self.calculate_shadow_position()  # Update shadow position when adjusting Z coordinate
