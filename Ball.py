from Renderizable import Renderizable
import pygame
import math

BALL_HEIGHT = 5
BALL_WIDTH = 5

class Ball(Renderizable):
    def __init__(self, x, y, game):
        # The ball is a 4x4 white square
        super().__init__(x, y, {"ball": pygame.Surface((BALL_WIDTH, BALL_HEIGHT))}, "ball")
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

    def move(self):
        self.y += self.y_speed
        self.x += self.x_speed
    
    def render(self, screen):
        if not self.hidden:
            screen.blit(self.image, (self.x, self.y))
    
    def reset_position(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.reset_speed()
        self.hide()

    def show(self):
        # Make the ball visible
        self.hidden = False

    def hide(self):
        # Hide the ball (make it transparent)
        self.hidden = True

    def fastball(self):
        self.y_speed = 10
        self.x_speed = 0
        self.move()

    def slider(self):
        self.y_speed = 10
        self.x_speed = 0.5
        self.move()
    
    def changeup(self):
        self.y_speed = 10
        self.x_speed = -0.25  # Change X to simulate movement
        self.move()
        # decrease speed
        self.y_speed *= 0.97  # Decrease speed with an exponential decay
        # Ensure y_speed never goes below a minimum threshold
        min_y_speed = 8  # Adjust this threshold as needed
        self.y_speed = max(self.y_speed, min_y_speed)
        self.y_speed = self.y_speed * 0.99  # Decrease speed
        
    def reset_speed(self):
        self.y_speed = 10
        self.x_speed = 0

    def hit_by_bat(self, pitch="?"):
        self.game.save_screenshot("contact")
        ball_center_x, ball_center_y = self.image.get_rect().center
        ball_center_y += self.y
        ball_center_x += self.x
        
        bat_center_y, bat_center_x = self.game.batter.baseball_bat.image.get_rect().center
        bat_center_x += self.game.batter.baseball_bat.x
        bat_center_y += self.game.batter.baseball_bat.y
        
        coordinates_text = f"""
        ball_center_y = {ball_center_y}
        ball_center_x = {ball_center_x}
        bat_center_y = {bat_center_y}
        bat_center_x = {bat_center_x}
        """
        print(coordinates_text)
        
        angle = math.atan2(ball_center_y - bat_center_y, ball_center_x - bat_center_x)
        
        print_text = f"""Pitch: {pitch}
        Angle: {angle}
        SEN: {math.sin(angle)}
        COS: {math.cos(angle)}"""
        print(print_text)
        
        self.x_speed = self.x_speed * math.cos(angle) + self.y_speed * math.cos(angle)
        self.y_speed = -1 * self.y_speed * math.sin(angle)
        
    def _animate_pitch(self, pitch):
        self.show()
        
        # GOING TOWARDS THE PLATE
        while self.y < 722 and not self.caught and not self.batted:
            pygame.time.delay(self.animation_delay)
            if (pitch == "fastball"):
                self.fastball()
            elif (pitch == "slider"):
                self.slider()
            elif (pitch == "changeup"):
                self.changeup()
        
        # CONTACT
        if self.batted:
            self.hit_by_bat(pitch=pitch)
            while self.y > 0: # HOME RUN
                self.move()
                pygame.time.delay(self.animation_delay)
            self.batted = False

        self.reset_position()
