# PYTHON MODULES
import pygame
import os
import sys
from datetime import datetime

# GAME MODULES
from Background import Park
from Ball import Ball
from Player import Batter, Pitcher
from Window import Window

directory_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(directory_path)

BATTER_INITIAL_X = 603
BATTER_INITIAL_Y = 663
BATTER_SPRITES = {
    "batter_stand" : pygame.image.load("assets/batter/batter_stand.png"),
    "batter_swing_1" : pygame.image.load("assets/batter/batter_swing_1.png"),
    "batter_swing_2" : pygame.image.load("assets/batter/batter_swing_2.png"),
    "batter_swing_3" : pygame.image.load("assets/batter/batter_swing_3.png"),
    "batter_swing_4" : pygame.image.load("assets/batter/batter_swing_4.png"),
    "batter_swing_5" : pygame.image.load("assets/batter/batter_swing_5.png")
}

PITCHER_INITIAL_X = 620
PITCHER_INITIAL_Y = 538
PITCHER_SPRITES = {
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

class Game:
    def save_screenshot(self, filename="print"):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_")
        pygame.image.save(self.window.screen, f"prints/{timestamp}{filename}.jpg")
    
    def update_display(self):
        self.window.render(gameObjects = [self.pitcher, self.batter, self.ball])
        pygame.display.flip()
    
    def __init__(self):
        # Game Elements
        self.batter = Batter(x=BATTER_INITIAL_X, y=BATTER_INITIAL_Y, sprites_dict=BATTER_SPRITES, game=self)
        self.pitcher = Pitcher(x=PITCHER_INITIAL_X, y=PITCHER_INITIAL_Y, sprites_dict=PITCHER_SPRITES, game=self)
        self.ball = Ball(639,554,game=self)
        self.park = Park()
        # Initialize game
        pygame.init()
        # Game window
        self.window = Window()
        
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
                    # PITCHES
                    if event.key == pygame.K_p:
                        self.pitcher.pitch(self.ball)
                    elif event.key == pygame.K_s:
                        self.pitcher.pitch(self.ball, pitch="slider")
                    elif event.key == pygame.K_c:
                        self.pitcher.pitch(self.ball, pitch="changeup")
                    elif event.key == pygame.K_b:
                        self.batter.bat(self.ball)

            self.update_display()
            # Cap the frame rate
            clock.tick(60)

        # Quit the game
        pygame.quit()
        sys.exit()

pass

Game()