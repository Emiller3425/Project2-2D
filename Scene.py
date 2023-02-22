
import pygame, sys
from pygame.locals import *
import sys
from Box2D import *
from GameObjects import *
import Engine as eg
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody)

# Creates the pygames window and holds all game objects
class Scene:

    updateables = []
    drawables = {}

    gravity = b2Vec2(0.5, -10.0)
    world = world(gravity, doSleep=False)
    
    def __init__(self):

        self.time_step = 1.0 / eg.Engine.frame_rate
        self.vel_iters, self.pos_iters = 6, 2


    def add_objects(self):
        """Creates an instance of all objects used in the game and adds them to the correct lists"""
        Scene.updateables.append(Updater(Scene.world, self.time_step, self.vel_iters, self.pos_iters))
        Scene.drawables.add(Ground(Scene.world, self._screen, 100, 100, 20, 20 ))

    def event_handler(self, event):
        pass


    def draw(self):
        pass


