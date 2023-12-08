from Renderizable import Renderizable
import pygame
import math

BALL_HEIGHT = 4
BALL_WIDTH = 4
GRAVITY = -1

class Ball(Renderizable):
    def __init__(self, x, y, z, game):
        self.radius = 2
        super().__init__(x, y, z, {"ball": pygame.Surface((self.radius*2, self.radius*2))}, "ball")
        self.game = game
        self.set_image()
        self.color = (255, 255, 255)
        self.image.fill(self.color)  # Fill the ball with white color
        self.initial_coordinates = [x,y,z]
        self.speed_vector = [0.5, 10, 0]
        self.hidden = True
        self.caught = False
        self.batted = False
        self.animation_delay = 100  # Adjust the delay to control animation speed

    def set_speed(self, speed_vector):
        for i in range(3):
            self.speed_vector[i] = speed_vector[i]

    def accelerate(self, acceleration_vector):
        """acceleration_vector = [x,y,z]"""
        for i in range(3):
            self.speed_vector[i] += acceleration_vector[i]

    def move(self):
        self.x += self.speed_vector[0]
        self.y += self.speed_vector[1]
        self.z += self.speed_vector[2]
        self.calculate_shadow_position()

    def adjust_z(self, delta_z):
        self.z += delta_z

    def calculate_shadow_position(self):
        # Calculate shadow position based on Z coordinate
        self.shadow_x = self.x
        self.shadow_y = self.y + self.shadow_offset * (self.z / 10)  # Adjust the factor as needed

    def render(self, screen):
        if not self.hidden:
            # Calculate size based on Z coordinate
            size_factor = max(1, 1 + self.z / 10)  # Adjust the factor as needed

            # Draw the ball with the calculated size
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius * size_factor))

            # Draw shadow
            pygame.draw.circle(screen, self.shadow_color, (int(self.shadow_x), int(self.shadow_y)), int(self.radius * size_factor))
    
    def reset_position(self):
        self.x, self.y, self.z = self.initial_coordinates
        self.reset_speed()
        self.hide()

    def show(self):
        # Make the ball visible
        self.hidden = False

    def hide(self):
        # Hide the ball (make it transparent)
        self.hidden = True

    def constant_speed_pitch_animation(self, speed_vector):
        self.set_speed(speed_vector)
        self.move()

    def fourseam_fastball_animation(self):
        fourseam_speed = [0,10,0]
        self.constant_speed_pitch_animation(fourseam_speed)

    def slider_animation(self):
        slider_speed = [0.5,10,0]
        self.constant_speed_pitch_animation(slider_speed)
    
    def decelerating_pitch_animation(self, speed_vector, acceleration_vector, minimum_speeds_vector):
        self.constant_speed_pitch_animation(speed_vector)
        self.accelerate(acceleration_vector)
        for i in range(3):
            self.speed_vector[i] = max(self.speed_vector[i], minimum_speeds_vector[i])
    
    def changeup(self):
        changeup_speed = [-0.25,10,0]
        changeup_acceleration = [0, self.speed_vector[1] * 0.03, 0]
        changeup_min_speed = [changeup_speed[0], 8, changeup_speed[2]]
        self.decelerating_pitch_animation(changeup_speed, changeup_acceleration, changeup_min_speed)
        
    def reset_speed(self):
        self.speed_vector[0] = 0
        self.speed_vector[1] = 10
        self.speed_vector[2] = 0

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
        Ball_z = {self.z}
        Angle: {angle}
        SEN: {math.sin(angle)}
        COS: {math.cos(angle)}"""
        print(print_text)
        
        self.speed_vector[0] = self.speed_vector[0] * math.cos(angle) + self.speed_vector[1] * math.cos(angle)
        self.speed_vector[1] = -1 * self.speed_vector[1] * math.sin(angle)
        
    def _animate_pitch(self, pitch):
        self.show()

        # GOING TOWARDS THE PLATE
        while self.y < 722 and not self.caught and not self.batted:
            pygame.time.delay(self.animation_delay)
            if pitch == "forseam_fastball":
                self.fourseam_fastball_animation()
            elif pitch == "slider":
                self.slider_animation()
            elif pitch == "changeup":
                self.changeup()
            self.calculate_shadow_position()  # Update shadow position when moving

        # CONTACT
        if self.batted:
            self.hit_by_bat(pitch=pitch)
            while self.y > 0:  # HOME RUN
                self.speed_vector[2] = 10
                self.move()
                pygame.time.delay(self.animation_delay)
            self.batted = False

        self.reset_position()
