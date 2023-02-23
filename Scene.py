
import pygame, sys
from pygame.locals import *
import sys
from Box2D import *
from GameObjects import *
import Engine as eg

# Creates the pygames window and holds all game objects
class Scene:

    updateables = []
    drawables = []

    gravity = b2Vec2(0.5, -10.0)
    world = b2World(gravity, doSleep=False)
    
    def __init__(self):
        
        self.time_step = 1.0 / eg.Engine.frame_rate
        self.vel_iters, self.pos_iters = 6, 2

        self.add_objects()


    def add_objects(self):
        """Creates an instance of all objects used in the game and adds them to the correct lists"""
        Scene.updateables.append(Updater(Scene.world, self.time_step, self.vel_iters, self.pos_iters))
        Scene.drawables.append(Ground(Scene.world, 0, 1, 25, .5 ))

    def event_handler(self, event):
        pass


    def draw(self):
        pass


