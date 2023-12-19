import pygame
from Background import Background
import os

directory_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(directory_path)
BG_SPRITES = {"stadium" : pygame.image.load(os.path.join(directory_path,"stadium.jpg"))}

class Window:
    def __init__(self):
        pygame.display.set_caption("Baseball Game")
        self.background = Background(x=0, y=0, sprites_dict=BG_SPRITES)
        w = self.background.image.get_width()
        h = self.background.image.get_height()
        self.screen = pygame.display.set_mode((w, h))
        self.strikeZone = StrikeZone()

    def render(self, renderList=[], radar_ball=False):
        for obj in renderList:
            obj.render(self.screen)
        
        if radar_ball:
            self.strikeZone.render(self.screen, radar_ball)


    pass

class StrikeZone:
    def __init__(self):
        # Coordenadas da zona de strike no estádio
        self.left = (636,689)
        self.right = (646,689)
        self.width = (self.right[0] - self.left[0])
        self.ball_distance_factor = 0

    # Projeção
    def render(self, screen, ball):
        # Customize this method based on your strike zone dimensions and appearance
        radar_color = (255, 255, 255)  # Color of the strike zone projection
        radar_width = 50  # Width of the strike zone projection
        radar_height = radar_width * 1.3  # Height of the strike zone projection
        radar_x = 800  # Arbitraty position
        radar_y = 642  # Place the zone at the bottom

        # Subdivide the strike zone into 9 rectangles
        subdivision_rows = 3
        subdivision_columns = 3
        gap = 2  # Gap between rectangles
        rectangle_width = (radar_width - (subdivision_columns - 1) * gap) / subdivision_columns
        rectangle_height = (radar_height - (subdivision_rows - 1) * gap) / subdivision_rows

        for row in range(subdivision_rows):
            for col in range(subdivision_columns):
                rect_x = radar_x + col * (rectangle_width + gap)
                rect_y = radar_y + row * (rectangle_height + gap)
                pygame.draw.rect(screen, radar_color, (rect_x, rect_y, rectangle_width, rectangle_height), 1)

        # Render the ball projection
        radar_ball_color = (0, 0, 0)
        
        relative_x = ((ball.x - self.left[0]) / self.width) * radar_width
        radar_ball_x = int(radar_x + relative_x)
        
        if ball.y > ball.initial_coordinates[1]:
            pitcher_distance = self.left[1] - ball.initial_coordinates[1]
            ball_distance = self.left[1] - ball.y
            travelled_distance_fraction = pitcher_distance / (ball_distance/pitcher_distance)
            self.ball_distance_factor = 2 + travelled_distance_fraction*11
        elif ball.y >= self.left[1]:
            print(self.ball_distance_factor)
        radar_ball_radius = 2 + self.ball_distance_factor
        
        radar_ball_y = int(radar_y + radar_height/2) # Alterar para variar conforme altura Z da bola

        pygame.draw.circle(screen, radar_ball_color, (radar_ball_x, radar_ball_y), radar_ball_radius)




    pass