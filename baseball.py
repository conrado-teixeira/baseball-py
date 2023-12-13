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
BALL_INITIAL_Z = 10

BATTER_INITIAL_X = 603
BATTER_INITIAL_Y = 663
BATTER_INITIAL_Z = 0
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
PITCHER_INITIAL_Z = 0
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
    def new_ab(self):
        self.setState("wait_4_pitch")
        if (self.curr_batter == 8):
            self.curr_batter = 0
        else:
            self.curr_batter += 1
        self.set_batter()

    def save_screenshot(self, filename="print"):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_")
        pygame.image.save(self.window.screen, f"prints/{timestamp}{filename}.jpg")
    
    def update_display(self):
        self.window.render([self.window.background])
        self.window.render(self.team_defense + self.team_offense)
        self.window.render([self.ball])
        pygame.display.flip()
    
    def setState(self, state):
        for k in  self.state.keys():
            self.state[k] = k == state

    def ball_is_hit(self):
        self.setState("batted")
        self.team_offense[self.curr_batter] = Runner(x=BATTER_INITIAL_X, y=BATTER_INITIAL_Y, sprites_dict=RUNNER_SPRITES, game=self)
        runner = self.team_offense[self.curr_batter]
        runner.run_to_base()     

    def set_batter(self):
        if (len(self.team_offense) <= self.curr_batter):
            self.team_offense.append(Batter(x=BATTER_INITIAL_X, y=BATTER_INITIAL_Y, sprites_dict=BATTER_SPRITES, game=self))
        else:
            self.team_offense[self.curr_batter] = Batter(x=BATTER_INITIAL_X, y=BATTER_INITIAL_Y, sprites_dict=BATTER_SPRITES, game=self)

    def restart_game(self):
        self.team_offense = []
        self.curr_batter = 0
        self.set_batter()
        self.team_defense = [
            Pitcher(x=PITCHER_INITIAL_X, y=PITCHER_INITIAL_Y, sprites_dict=PITCHER_SPRITES, game=self)
        ]
        self.batter = self.team_offense[self.curr_batter]
        self.pitcher = self.team_defense[0]
        self.ball = Ball(BALL_INITIAL_X, BALL_INITIAL_Y, BALL_INITIAL_Z, game=self)
        self.park = Park()

    def run_game_loop(self):
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
                        self.pitcher.pitch("4s_fastball")
                    elif event.key == pygame.K_s:
                        self.pitcher.pitch("slider")
                    elif event.key == pygame.K_c:
                        self.pitcher.pitch("changeup")
                    elif event.key == pygame.K_b:
                        self.batter.bat()
                        self.batter.bat()
                    elif event.key == pygame.K_UP:
                        print(event.key)
                    elif event.key == pygame.K_DOWN:
                        print(event.key)
                    elif event.key == pygame.K_LEFT:
                        self.pitcher.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.pitcher.move_right()
                    elif event.key == pygame.K_h:
                        self.batter.bat("bunt_C")
                    elif event.key == pygame.K_g:
                        self.batter.bat("bunt_L")
                    elif event.key == pygame.K_j:
                        self.batter.bat("bunt_R")
                    elif event.key == pygame.K_PAGEUP:
                        self.ball.move([0,0,10])
                    elif event.key == pygame.K_PAGEDOWN:
                        self.ball.move([0,0,-10])
                    elif event.key == pygame.K_r:
                        # Restart the game when 'R' is pressed
                        self.restart_game()

            self.update_display()
            # Cap the frame rate
            clock.tick(60)
            
    def __init__(self):
        # Game State
        self.state = {
            "wait_4_pitch" : True,
            "pitch" : False,
            "batted" : False
        }
        # Game Elements
        self.team_offense = []
        self.curr_batter = 0
        self.set_batter()
        self.team_defense = [
            Pitcher(x=PITCHER_INITIAL_X, y=PITCHER_INITIAL_Y, sprites_dict=PITCHER_SPRITES, game=self)
        ]
        self.batter = self.team_offense[self.curr_batter]
        self.pitcher = self.team_defense[0]
        self.ball = Ball(BALL_INITIAL_X,BALL_INITIAL_Y,10,game=self)
        self.park = Park()
        # Initialize game
        pygame.init()
        # Game window
        self.window = Window()
        
        
        

        self.run_game_loop()

        # Quit the game
        pygame.quit()
        sys.exit()

pass

Game()