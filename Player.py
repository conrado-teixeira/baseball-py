from Renderizable import Renderizable
from threading import Thread  # Import Thread for concurrent animations
import pygame

def rotate_around_center(surface, angle, center_x, center_y):
    rotated_surface = pygame.transform.rotate(surface, angle)
    rotated_rect = rotated_surface.get_rect()
    rotated_rect.center = (center_x, center_y)
    return rotated_surface

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
            self.curr_sprite = f"swing_{swing_step}"
            self.set_image()
            if swing_step == 2:
                self.x = self.initial_x+10
                self.y = self.initial_y+20 
            elif swing_step == 3:
                self.x = self.initial_x+12
                self.y = self.initial_y+18
            elif swing_step == 4:
                self.x = self.initial_x+12
                self.y = self.initial_y+8
            #else:
            #    self.x = self.initial_x
            #    self.y = self.initial_y+20 

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
        if self.batting and not ball.caught and not ball.batted and not ball.hidden:
            # Check if the ball's Y coordinate is close to the batter's Y coordinate
            if abs(ball.y - self.y) < 10:  # Adjust this value for the hit tolerance
                ball.batted = True

    def bat(self, ball):
        if not self.batting:
            self.batting = True
            thread = Thread(target=self._animate_batting, args=[ball, self.game])
            thread.start()# Animate the batting action

    def _animate_batting(self,ball, game):
        animation = [
            self.curr_sprite,
            "batter_swing_1",
            "batter_swing_2",
            "batter_swing_3",
            "batter_swing_4",
            "batter_swing_5",
            "batter_swing_5",
            "batter_swing_5",
            "batter_swing_5",
            "batter_stand"
        ]
        for frame in animation:
            self.curr_sprite = frame
            if (self.curr_sprite in ["batter_swing_2","batter_swing_3","batter_swing_4"]):
                self.baseball_bat.position_swing(int(self.curr_sprite[-1]))
                # Lógica antiga de rebatida
                if abs(ball.y - self.y) < 10:  # Adjust this value for the hit tolerance
                    ball.batted = True
            self.set_image()
            game.update_display()  # Render the frame
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

    def pitch(self, ball, pitch="fastball"):
        if not self.pitching:
            self.pitching = True
            thread = Thread(target=self._animate_pitch(ball, pitch, self.game))
            thread.start()# Animate the batting action

    def _animate_pitch(self, ball, pitch, game):
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
            game.update_display()  # Render the frame
            if i == 4:
                # Show the ball at the specified position on the fourth step
                thread = Thread(target=ball._animate_pitch, args=[pitch])
                thread.start()# Animate the batting action
            pygame.time.delay(self.animation_delay)  # Delay to control animation speed
        # Volta pra posição inicial            
        self.pitching = False  # Reset the flag when animation is complete
