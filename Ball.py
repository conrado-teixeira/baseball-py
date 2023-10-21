from Renderizable import Renderizable
import pygame

class Ball(Renderizable):
    def __init__(self, x, y):
        # The ball is a 4x4 white square
        super().__init__(x, y, {"ball": pygame.Surface((4, 4))}, "ball")
        self.set_image()
        self.image.fill((255, 255, 255))  # Fill the ball with white color
        self.initial_x = x  # Store the initial Y coordinate
        self.initial_y = y  # Store the initial Y coordinate
        self.vertical_speed = 10  # Adjust this value to control the pitch speed
        self.hidden = True
        self.caught = False
        self.batted = False
        self.animation_delay = 100  # Adjust the delay to control animation speed

    def render(self, screen):
        if not self.hidden:
            screen.blit(self.image, (self.x, self.y))
    
    def reset_position(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.hide()

    def show(self):
        # Make the ball visible
        self.hidden = False

    def hide(self):
        # Hide the ball (make it transparent)
        self.hidden = True

    def _animate_pitch(self, pitch):
        self.show()
        while self.y < 722 and not self.caught and not self.batted:
            pygame.time.delay(self.animation_delay)
            if (pitch == "fastball"):
                self.y += self.vertical_speed  # Increase Y to simulate the pitch
            elif (pitch == "slider"):
                self.y += self.vertical_speed  # Increase Y to simulate the pitch
                self.x += 0.5  # Increase X to simulate movement
            elif (pitch == "changeup"):
                self.y += self.vertical_speed * 0.8  # Increase Y to simulate the pitch
                self.vertical_speed = self.vertical_speed * 0.99  # Decrease speed
                self.x -= 0.25  # Increase X to simulate movement
        if self.batted:
            while self.y > 0:
                pygame.time.delay(self.animation_delay)
                self.y -= self.vertical_speed  # Increase Y to simulate the pitch
            self.batted = False

        self.vertical_speed = 10
        self.reset_position()
