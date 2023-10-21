from Renderizable import Renderizable
from threading import Thread  # Import Thread for concurrent animations
import pygame

class Player(Renderizable):
    def __init__(self, x, y, sprites_dict, initial_sprite):
        super().__init__(x, y, sprites_dict, initial_sprite)
        
class Batter(Player):
    def __init__(self, x, y, sprites_dict, game):
        self.game = game
        super().__init__(x, y, sprites_dict, "batter_stand")
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
            "batter_stand"
        ]
        for frame in animation:
            self.curr_sprite = frame
            if (self.curr_sprite in ["batter_swing_2","batter_swing_3","batter_swing_4"]):
                if abs(ball.y - self.y) < 10:  # Adjust this value for the hit tolerance
                    ball.batted = True
            self.set_image()
            pygame.time.delay(self.animation_delay)
            game.update_display()  # Render the frame
        # Reset the flag when animation is complete
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
            pygame.time.delay(self.animation_delay)  # Delay to control animation speed
            game.update_display()  # Render the frame
            if i == 4:
                # Show the ball at the specified position on the fourth step
                thread = Thread(target=ball._animate_pitch, args=[pitch])
                thread.start()# Animate the batting action
        # Volta pra posição inicial            
        self.pitching = False  # Reset the flag when animation is complete
