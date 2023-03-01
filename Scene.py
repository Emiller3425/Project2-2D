
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

    groundGroup = pygame.sprite.Group()

    gravity = b2Vec2(0, -10.0)
    world = b2World(gravity, doSleep=False)

    
    def __init__(self):
        
        self.time_step = 1.0 / eg.Engine.frame_rate
        self.vel_iters, self.pos_iters = 6, 2

        self.add_objects()


    def add_objects(self):
        """Creates an instance of all objects used in the game and adds them to the correct lists"""
        Scene.updateables.append(Updater(self.time_step, self.vel_iters, self.pos_iters))

        player1 = Player(1)
        player2 = Player(2)

        Scene.updateables.append(player1)
        Scene.drawables.append(player1)

        Scene.updateables.append(player2)
        Scene.drawables.append(player2)

        self.add_platforms()


    def add_platforms(self):
        floor = Ground(0, 7.4, 25, .2 )
        ceiling = Ground(0, 0, 25, .2 )
        rightWall = Ground(10.1, 0, .1, 25 )
        leftWall = Ground(0, 0, .08, 25 )
        bottomOfMiddleArea = Ground(4, 5.8, 5, .15 )
        #secondLayerPlatform = Ground(0, 4, 4, .2 )

        Scene.groundGroup.add(floor)
        #Scene.groundGroup.add(ceiling)
        #Scene.groundGroup.add(rightWall)
        #Scene.groundGroup.add(leftWall)
        Scene.groundGroup.add(bottomOfMiddleArea)
        #Scene.groundGroup.add(secondLayerPlatform)

        Scene.drawables.append(floor)
        Scene.drawables.append(ceiling)
        Scene.drawables.append(rightWall)
        Scene.drawables.append(leftWall)
        Scene.drawables.append(bottomOfMiddleArea)
       # Scene.drawables.append(secondLayerPlatform)



