import pygame
import os
import sys
from threading import Thread  # Import Thread for concurrent animations

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

class Background(Renderizable):
    def __init__(self, x, y, sprites_dict):
        super().__init__(x, y, sprites_dict, "stadium")

class Player(Renderizable):
    def __init__(self, x, y, sprites_dict, initial_sprite):
        super().__init__(x, y, sprites_dict, initial_sprite)

class Batter(Player):
    def __init__(self, x, y, sprites_dict):
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
            thread = Thread(target=self._animate_batting, args=[ball])
            thread.start()# Animate the batting action

    def _animate_batting(self,ball):
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
            window.render()
            pygame.display.flip()
        # Reset the flag when animation is complete
        self.batting = False


class Pitcher(Player):
    def __init__(self, x, y, sprites_dict):
        super().__init__(x, y, sprites_dict, "pitcher_stand_c")
        self.pitching = False  # Flag to control the animation
        self.animation_delay = 100  # Adjust the delay to control animation speed

    def pitch(self, ball, pitch="fastball"):
        if not self.pitching:
            self.pitching = True
            thread = Thread(target=self._animate_pitch(ball, pitch))
            thread.start()# Animate the batting action

    def _animate_pitch(self, ball, pitch):
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
            window.render()  # Render the frame
            if i == 4:
                # Show the ball at the specified position on the fourth step
                thread = Thread(target=ball._animate_pitch, args=[pitch])
                thread.start()# Animate the batting action
            pygame.display.flip()  # Update the display
        # Volta pra posição inicial            
        self.pitching = False  # Reset the flag when animation is complete

class Base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hasRunner = False

class Park:
    def __init__(self):
        self.bases = []
        # Home
        self.bases.append(Base(0, 0))
        # 1
        self.bases.append(Base(0, 0))
        # 2
        self.bases.append(Base(0, 0))
        # 3
        self.bases.append(Base(0, 0))

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

class Window:
    def __init__(self):
        pygame.display.set_caption("Baseball Game")
        bg_sprites = {"stadium" : pygame.image.load("stadium.jpg")}
        self.background = Background(x=0, y=0, sprites_dict=bg_sprites)
        w = self.background.image.get_width()
        h = self.background.image.get_height()
        self.screen = pygame.display.set_mode((w, h))
        self.ball = Ball(639,554)
        self.add_players()

    def add_players(self):
        self.team_A = []
        batter_sprites = {
            "batter_stand" : pygame.image.load("assets/batter/batter_stand.png"),
            "batter_swing_1" : pygame.image.load("assets/batter/batter_swing_1.png"),
            "batter_swing_2" : pygame.image.load("assets/batter/batter_swing_2.png"),
            "batter_swing_3" : pygame.image.load("assets/batter/batter_swing_3.png"),
            "batter_swing_4" : pygame.image.load("assets/batter/batter_swing_4.png"),
            "batter_swing_5" : pygame.image.load("assets/batter/batter_swing_5.png")
        }
        batter = Batter(x=603, y=663, sprites_dict=batter_sprites)
        self.team_A.append(batter)

        self.team_B = []
        pitcher_sprites = {
            "pitcher_look_c" : pygame.image.load("assets/pitcher/pitcher_look_c.png"),
            "pitcher_look_r" : pygame.image.load("assets/pitcher/pitcher_look_r.png"),
            "pitcher_pick_l" : pygame.image.load("assets/pitcher/pitcher_pick_l.png"),
            "pitcher_pick_r" : pygame.image.load("assets/pitcher/pitcher_pick_r.png"),
            "pitcher_pick_r_lh" : pygame.image.load("assets/pitcher/pitcher_pick_r_lh.png"),
            "pitcher_pitch_1" : pygame.image.load("assets/pitcher/pitcher_pitch_1.png"),
            "pitcher_pitch_2" : pygame.image.load("assets/pitcher/pitcher_pitch_2.png"),
            "pitcher_pitch_3" : pygame.image.load("assets/pitcher/pitcher_pitch_3.png"),
            "pitcher_pitch_4" : pygame.image.load("assets/pitcher/pitcher_pitch_4.png"),
            "pitcher_stand_c" : pygame.image.load("assets/pitcher/pitcher_stand_c.png"),
            "pitcher_stand_r" : pygame.image.load("assets/pitcher/pitcher_stand_r.png")
        }
        pitcher = Pitcher(x=620, y=538, sprites_dict=pitcher_sprites)
        self.team_B.append(pitcher)

    def render(self):
        self.background.render(self.screen)
        if not self.ball.hidden:
            self.ball.render(self.screen)
        for player in self.team_A + self.team_B:
            player.render(self.screen)

# Set Working Directory
directory_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(directory_path)

# Initialize Pygame
pygame.init()

# Create the game window
window = Window()

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the position of the mouse click
            x, y = pygame.mouse.get_pos()
            print(f"Clicked at position X:{x}, Y:{y}")
            # Check for the 'P' key press event
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                # If 'P' is pressed, change the pitcher's sprite
                for pitcher in window.team_B:
                    if isinstance(pitcher, Pitcher):
                        pitcher.pitch(window.ball)
            elif event.key == pygame.K_s:
                # If 'P' is pressed, change the pitcher's sprite
                for pitcher in window.team_B:
                    if isinstance(pitcher, Pitcher):
                        pitcher.pitch(window.ball, pitch="slider")
            elif event.key == pygame.K_c:
                # If 'P' is pressed, change the pitcher's sprite
                for pitcher in window.team_B:
                    if isinstance(pitcher, Pitcher):
                        pitcher.pitch(window.ball, pitch="changeup")
            elif event.key == pygame.K_b:
                # If 'P' is pressed, change the pitcher's sprite
                for batter in window.team_A:
                    if isinstance(batter, Batter):
                        batter.bat(window.ball)

    # Draw the background image
    window.render()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
sys.exit()
