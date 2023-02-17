
import pygame, sys
from pygame.locals import *
import random
import sys
from Scene import Scene
from pygame.time import *
import math


# Engine class that creates the clock and scene for the game
# Has a loop method which runs the game as long as self._running is true
class Engine:

    delta_time = 0
    events = None
    current_scene = None

    def __init__(self, width=1024, height=768):
        pygame.init()

        self.color = (0,0,0)
        self.title = "2D Game"
        # size of the screen
        self.screen_width = width
        self.screen_height = height

        self._screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(self.title)
        self._screen.fill(self.color)

        # determines if the game loop is running or not
        self._running = False

        self._clock = pygame.time.Clock()

        # Changable frame rate variable for frame limiting
        self.frame_rate = 60

        # initializes the scene for the game
        self.current_scene = Scene()


    def loop(self):
        """ Main game loop that handles events, frame limiting, scene updates, and scene drawing """

        self._running = True

        while self._running:
            # loops through all events in the current game iteration
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                

            #Frame limiting
            # the following code will frame limit to whatever frame_rate is set 
            Engine.delta_time = self._clock.tick(self.frame_rate) / 1000

            pygame.display.flip
            pygame.display.update()

