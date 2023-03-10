
import pygame, sys
from pygame.locals import *
import random
import sys
from Scene import Scene
from pygame.time import *
import math
from Box2D import *


# Engine class that creates the clock and scene for the game
# Has a loop method which runs the game as long as self._running is true
class Engine:

    delta_time = 0
    events = None
    current_scene = None
    screen = None
    # Changable frame rate variable for frame limiting
    frame_rate = 60 

    def __init__(self, width=1024, height=768):
        pygame.init()

        self.color = (50,50,50)
        self.title = "2D Game"
        # size of the screen
        self.screen_width = width
        self.screen_height = height

        self._screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(self.title)
        self._screen.fill(self.color)

        Engine.screen = self._screen

        # determines if the game loop is running or not
        self._running = False

        self._clock = pygame.time.Clock()

        # initializes the scene for the game
        Engine.current_scene = Scene()


    def loop(self):
        """ Main game loop that handles events, frame limiting, scene updates, and scene drawing """

        self._running = True

        while self._running:

            self._screen.fill(self.color)

            Engine.events = pygame.event.get()
            # loops through all events in the current game iteration
            for event in Engine.events:
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
            #Update game world
            for updateable in Engine.current_scene.updateables:
                updateable.update(self.delta_time)

            #Draw game world
            for drawable in Engine.current_scene.drawables:
                drawable.draw(self._screen)

            #Frame limiting
            # the following code will frame limit to whatever frame_rate is set 
            Engine.delta_time = self._clock.tick(Engine.frame_rate) / 1000

            pygame.display.flip()
            pygame.display.update()

    def end(self):
        """Shutdown PyGame and return the memory."""
        pygame.quit()

