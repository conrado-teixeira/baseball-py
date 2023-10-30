# PYTHON MODULES
import pygame
import os
import sys
from datetime import datetime

# GAME MODULES
from Background import Park
from Ball import Ball
from Player import Batter, Pitcher, Runner
from Window import Window

directory_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(directory_path)

BALL_INITIAL_X = 636
BALL_INITIAL_Y = 554

BATTER_INITIAL_X = 603
BATTER_INITIAL_Y = 663
BATTER_SPRITES = {
    "batter_stand" : pygame.image.load("assets/batter/batter_stand.png"),
    "batter_swing_1" : pygame.image.load("assets/batter/batter_swing_1.png"), #windup
    "batter_swing_2" : pygame.image.load("assets/batter/batter_swing_2.png"), # early
    "batter_swing_3" : pygame.image.load("assets/batter/batter_swing_3.png"), # perfect
    "batter_swing_4" : pygame.image.load("assets/batter/batter_swing_4.png"), # late
    "batter_swing_5" : pygame.image.load("assets/batter/batter_swing_5.png") # final
}

PITCHER_INITIAL_X = 617
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

RUNNER_SPRITES = {
    "runner_run_dr_1" : pygame.image.load("assets/runner/runner_run_dr_1.png"),
    "runner_run_dr_2" : pygame.image.load("assets/runner/runner_run_dr_2.png"),
    "runner_run_dr_3" : pygame.image.load("assets/runner/runner_run_dr_3.png"),
    "runner_run_ur_1" : pygame.image.load("assets/runner/runner_run_ur_1.png"),
    "runner_run_ur_2" : pygame.image.load("assets/runner/runner_run_ur_2.png"),
    "runner_run_ur_3" : pygame.image.load("assets/runner/runner_run_ur_3.png"),
    "runner_stand" : pygame.image.load("assets/runner/runner_stand.png")
}

class Game:
    def save_screenshot(self, filename="print"):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_")
        pygame.image.save(self.window.screen, f"prints/{timestamp}{filename}.jpg")
    
    def update_display(self):
        self.window.render(gameObjects = [self.team_defense, self.team_offense, self.ball])
        pygame.display.flip()
    
    def ball_is_hit(self):
        self.team_offense[self.curr_batter] = Runner(x=BATTER_INITIAL_X, y=BATTER_INITIAL_Y, sprites_dict=RUNNER_SPRITES, game=self)
        runner = self.team_offense[self.curr_batter]
        runner.run_to_base()
        if (self.curr_batter == 9):
            self.curr_batter = 0
        else:
            self.curr_batter += 1      

    def set_batter(self):
        if (len(self.team_offense) <= self.curr_batter):
            self.team_offense.append(Batter(x=BATTER_INITIAL_X, y=BATTER_INITIAL_Y, sprites_dict=BATTER_SPRITES, game=self))
        else:
            self.team_offense[self.curr_batter] = Batter(x=BATTER_INITIAL_X, y=BATTER_INITIAL_Y, sprites_dict=BATTER_SPRITES, game=self)

    def __init__(self):
        # Game Elements
        self.team_offense = []
        self.curr_batter = 0
        self.set_batter()
        self.team_defense = [
            Pitcher(x=PITCHER_INITIAL_X, y=PITCHER_INITIAL_Y, sprites_dict=PITCHER_SPRITES, game=self)
        ]
        self.batter = self.team_offense[self.curr_batter]
        self.pitcher = self.team_defense[0]
        self.ball = Ball(BALL_INITIAL_X,BALL_INITIAL_Y,game=self)
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
                        self.pitcher.pitch()
                    elif event.key == pygame.K_s:
                        self.pitcher.pitch("slider")
                    elif event.key == pygame.K_c:
                        self.pitcher.pitch("changeup")
                    elif event.key == pygame.K_b:
                        self.batter.bat()
                    elif event.key == pygame.K_UP:
                        self.batter.bat("bunt_C")
                    elif event.key == pygame.K_LEFT:
                        self.batter.bat("bunt_L")
                    elif event.key == pygame.K_RIGHT:
                        self.batter.bat("bunt_R")

            self.update_display()
            # Cap the frame rate
            clock.tick(60)

        # Quit the game
        pygame.quit()
        sys.exit()

pass

Game()