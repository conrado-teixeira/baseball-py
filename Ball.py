from Renderizable import Renderizable
import pygame
import math

class Ball(Renderizable):
    def __init__(self, x, y, game):
        # The ball is a 4x4 white square
        super().__init__(x, y, {"ball": pygame.Surface((4, 4))}, "ball")
        self.game = game
        self.set_image()
        self.image.fill((255, 255, 255))  # Fill the ball with white color
        self.initial_x = x  # Store the initial Y coordinate
        self.initial_y = y  # Store the initial Y coordinate
        self.y_speed = 10  # Adjust this value to control the pitch speed
        self.x_speed = 0.5 # Adjust this value to control the pitch speed
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
                self.y += self.y_speed  # Increase Y to simulate the pitch
            elif (pitch == "slider"):
                self.y += self.y_speed  # Increase Y to simulate the pitch
                self.x += self.x_speed  # Increase X to simulate movement
            elif (pitch == "changeup"):
                self.y += self.y_speed * 0.8  # Increase Y to simulate the pitch
                self.y_speed = self.y_speed * 0.99  # Decrease speed
                self.x -= self.x_speed/2  # Change X to simulate movement
        if self.batted:
            angle = math.atan2(self.y - self.game.batter.baseball_bat.y, self.x - self.game.batter.baseball_bat.x)
            print(angle)
            batted_x_speed = self.x_speed * math.cos(angle) + self.y_speed * math.cos(angle)
            print(f"batted_x_speed = {batted_x_speed}")
            batted_y_speed = self.y_speed * math.sin(angle)
            print(f"batted_y_speed = {batted_y_speed}")
            while self.y > 0: # HOME RUN
                self.y -= batted_y_speed  
                self.x -= batted_x_speed
                pygame.time.delay(self.animation_delay)
            self.batted = False

        self.y_speed = 10
        self.reset_position()
