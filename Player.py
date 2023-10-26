from Renderizable import Renderizable
from threading import Thread  # Import Thread for concurrent animations
import pygame

# def rotate_around_center(surface, angle, center_x, center_y):
#     rotated_surface = pygame.transform.rotate(surface, angle)
#     rotated_rect = rotated_surface.get_rect()
#     rotated_rect.center = (center_x, center_y)
#     return rotated_surface

class Player(Renderizable):
    def __init__(self, x, y, sprites_dict, initial_sprite):
        super().__init__(x, y, sprites_dict, initial_sprite)
        
class BaseballBat(Renderizable):
    def __init__(self, x, y):
        # Create the sprites
        bat_stand = pygame.Surface((2, 20))
        bat_swing_3 = pygame.Surface((13, 2))

        # Fill the sprites with a color
        color = (255, 0, 0)
        bat_stand.fill(color)
        bat_swing_3.fill(color)

        # Create the bat image when diagonal
        bat_swing_2 = pygame.Surface((13, 2), pygame.SRCALPHA)
        bat_swing_2.fill(color)
        bat_swing_2 = pygame.transform.rotate(bat_swing_2, -30)
        
        # Create the bat image when diagonal
        bat_swing_4 = pygame.Surface((11, 2), pygame.SRCALPHA)
        bat_swing_4.fill(color)
        bat_swing_4 = pygame.transform.rotate(bat_swing_4, 30)

        # Store the sprites in a dictionary
        sprites = {
            "stand": bat_stand,
            "swing_2": bat_swing_2,
            "swing_3": bat_swing_3,
            "swing_4": bat_swing_4
        }

        super().__init__(x, y, sprites, "stand")
        self.initial_x = x
        self.initial_y = y
        self.hidden = True
        self.animation_delay = 100

    def reset_position(self):
        self.curr_sprite = "stand"
        self.x = self.initial_x
        self.y = self.initial_y
        self.set_image()

    def position_swing(self, swing_step):
        if swing_step in [2, 3, 4]:
            if swing_step == 2:
                self.x = self.initial_x+10
                self.y = self.initial_y+20 
            elif swing_step == 3:
                self.x = self.initial_x+12
                self.y = self.initial_y+18
            elif swing_step == 4:
                self.x = self.initial_x+12
                self.y = self.initial_y+8
            self.curr_sprite = f"swing_{swing_step}"
            self.set_image()

    def get_bat_rect(self):
        angle = 0
        if self.curr_sprite == "swing_2":
            angle = -30
        elif self.curr_sprite == "swing_4":
            angle = 30
        bat_rect = self.image.get_rect()  # Use the image attribute of the baseball_bat
        bat_rect.topleft = (self.x, self.y)  # Set the position of the Rect
        return bat_rect
    
    def render(self, screen):
        if not self.hidden:
            screen.blit(self.image, (self.x, self.y))

class Batter(Player):
    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.baseball_bat.render(screen)
    
    def __init__(self, x, y, sprites_dict, game):
        super().__init__(x, y, sprites_dict, "batter_stand")
        self.game = game
        self.baseball_bat = BaseballBat(x+20,y+3)
        self.batting = False
        self.animation_delay = 100  # Adjust the delay to control animation speed

    def check_for_hit(self, ball):
        if self.batting and not ball.caught and not ball.batted:
            ball_rect = pygame.Rect(ball.x, ball.y, ball.image.get_width(), ball.image.get_height())
            bat_rect = self.baseball_bat.get_bat_rect()
            if ball_rect.colliderect(bat_rect):
                ball.batted = True
                print(f"CONTACT AT {self.curr_sprite}!")
            else:
                self.no_contact += 1
                if self.no_contact == 3:
                    print("STRIKE!")
                    self.game.save_screenshot("swing_n_miss")

    def bat(self, swing="swing"):
        if not self.batting:
            self.batting = True
            self.no_contact = 0
            thread = Thread(target=self._animate_batting, args=[swing])
            thread.start()# Animate the batting action

    def _animate_batting(self,swing):
        ball = self.game.ball
        animations = {
            "bunt_C" : ["batter_stand", "batter_swing_3", "batter_swing_3", "batter_swing_3", "batter_swing_3", "batter_swing_3", "batter_stand"],
            "bunt_L" : ["batter_stand", "batter_swing_4", "batter_swing_4", "batter_swing_4", "batter_swing_4", "batter_swing_4", "batter_stand"],
            "bunt_R" : ["batter_stand", "batter_swing_2", "batter_swing_2", "batter_swing_2", "batter_swing_2", "batter_swing_2", "batter_stand"],
            "swing" : ["batter_stand", "batter_swing_1", "batter_swing_2", "batter_swing_3", "batter_swing_4", "batter_swing_5", "batter_swing_5", "batter_swing_5", "batter_swing_5", "batter_stand"],
        }
        for frame in animations[swing]:
            self.curr_sprite = frame
            self.set_image()
            self.game.update_display()  # Render the frame
            if (self.curr_sprite in ["batter_swing_2","batter_swing_3","batter_swing_4"]):
                self.baseball_bat.position_swing(int(self.curr_sprite[-1]))
                self.check_for_hit(ball)
            pygame.time.delay(self.animation_delay)
        # Reset the flag when animation is complete
        self.baseball_bat.reset_position() # DESCOMENTAR PRA VOLTAR A ANIMAÇÃO
        self.batting = False


class Pitcher(Player):
    def __init__(self, x, y, sprites_dict, game):
        super().__init__(x, y, sprites_dict, "pitcher_stand_c")
        self.pitching = False  # Flag to control the animation
        self.animation_delay = 100  # Adjust the delay to control animation speed
        self.game = game

    def pitch(self, pitch="fastball"):
        if self.game.ball.x == self.game.ball.initial_x and self.game.ball.y == self.game.ball.initial_y:
            self.pitching = True
            thread = Thread(target=self._animate_pitch(pitch))
            thread.start()# Animate the batting action

    def _animate_pitch(self, pitch):
        animation = [
            self.curr_sprite,
            "pitcher_pitch_1",
            "pitcher_pitch_2",
            "pitcher_pitch_3",
            "pitcher_pitch_4",
            "pitcher_pitch_4",
            "pitcher_pitch_4",
            "pitcher_pitch_4",
            "pitcher_stand_c"
        ]
        i = 0
        for frame in animation:
            i += 1
            self.curr_sprite = frame
            self.set_image()
            self.game.update_display()  # Render the frame
            if i == 4:
                # Show the ball at the specified position on the fourth step
                thread = Thread(target=self.game.ball._animate_pitch, args=[pitch])
                thread.start()# Animate the batting action
            pygame.time.delay(self.animation_delay)  # Delay to control animation speed
        # Volta pra posição inicial            
        self.pitching = False  # Reset the flag when animation is complete
