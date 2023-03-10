
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
    doorGroup = pygame.sprite.Group()
    buttonGroup = pygame.sprite.Group()

    gravity = b2Vec2(0, -10.0)
    world = b2World(gravity, doSleep=False)

    
    def __init__(self):
        
        self.time_step = 1.0 / eg.Engine.frame_rate
        self.vel_iters, self.pos_iters = 6, 2

        self.add_objects()


    def reset_players(self):
        self.player1.reset()
        self.player2.reset()

    def check_win(self):
        if self.player1.atFinalDoor and self.player2.atFinalDoor:
            button = Button(200, 1000, Color(255,255,255), eg.Engine.screen, 80, 50, 'Made by: Josh Fletcher and Ethan Miller', (0, 0, 0), (255,255,255), 'timesnewroman', 50)
            button.draw()

    def add_objects(self):
        """Creates an instance of all objects used in the game and adds them to the correct lists"""
        Scene.updateables.append(Updater(self.time_step, self.vel_iters, self.pos_iters))

        self.player1 = Player(1)
        self.player2 = Player(2)

        player1Door = Door(4, 3, 1)
        player2Door = Door(6, 3, 2)

        leftBottomButton = GroundButton(.55, 3.6, 2)
        rightBottomButton = GroundButton(9.5, 3.6, 1)

        leftTopButton = GroundButton(3, 6.1, 2)
        rightTopButton = GroundButton(7, 6.1, 1)

        Scene.drawables.append(leftBottomButton)
        Scene.drawables.append(rightBottomButton)
        Scene.drawables.append(leftTopButton)
        Scene.drawables.append(rightTopButton)
        Scene.buttonGroup.add(leftBottomButton)
        Scene.buttonGroup.add(rightBottomButton)
        Scene.buttonGroup.add(leftTopButton)
        Scene.buttonGroup.add(rightTopButton)

        Scene.doorGroup.add(player1Door)
        Scene.doorGroup.add(player2Door)

        Scene.drawables.append(player1Door)
        Scene.drawables.append(player2Door)

        Scene.updateables.append(self.player1)
        Scene.drawables.append(self.player1)

        Scene.updateables.append(self.player2)
        Scene.drawables.append(self.player2)

        self.add_platforms()


    def buttonPress(self, type):
        if type == 1:
            self.moveableLeftPlatform.move(2)
        elif type == 2:
            self.moveableRightPlatform.move(8)

    def buttonUnpress(self, type):
        if type == 1:
            self.moveableLeftPlatform.move(4)
        elif type == 2:
            self.moveableRightPlatform.move(6)

    def add_platforms(self):
        ceiling = Ground(0, 7.6, 25, .5, 0)
        floor = Ground(0, 0, 25, .5, 0)
        rightWall = Ground(10.1, 0, .5, 25, 0)
        leftWall = Ground(0, 0, .5, 25, 0)

        leftSidePlatform = Ground(0, 1.5, 3, .2, 0)
        rightSidePlatform = Ground(10.1, 1.5, 3, .2, 0)

        leftSidePlatformTop = Ground(0, 3.5, 3, .2, 0)
        rightSidePlatformTop = Ground(10.1, 3.5, 3, .2, 0)

        largeBottomMiddlePlatform = Ground(5, 2.5, 6.5, .25, 0)

        leftPole = Ground(3, 4.2, .2, 3.5, 0)
        rightPole = Ground(7, 4.2, .2, 3.5, 0)

        topOfLeftPolePlatform = Ground(3, 6, 2, .2, 0)
        topOfRightPolePlatform = Ground(7, 6, 2, .2, 0)

        betweenDoorsPlatform = Ground(5, 4, 1.2, .2, 0)

        bottomGreenArea = Ground(5, .1, 4, .5, 3)

        jumpPlatformLeft = Ground(4, .8, 1, .1, 0)
        jumpPlatformRight = Ground(6, .8, 1, .1, 0)

        leftBluePlatform = Ground(2.3, 2.6, 1, .1, 2)
        rightRedPlatform = Ground(7.7, 2.6, 1, .1, 1)

        self.moveableLeftPlatform = Ground(4, 5, 1, .2, 0)
        self.moveableRightPlatform = Ground(6, 5, 1, .2, 0)

        Scene.groundGroup.add(floor)
        Scene.groundGroup.add(ceiling)
        Scene.groundGroup.add(rightWall)
        Scene.groundGroup.add(leftWall)
        Scene.groundGroup.add(leftSidePlatform)
        Scene.groundGroup.add(rightSidePlatform)
        Scene.groundGroup.add(leftSidePlatformTop)
        Scene.groundGroup.add(rightSidePlatformTop)
        Scene.groundGroup.add(largeBottomMiddlePlatform)
        Scene.groundGroup.add(leftPole)
        Scene.groundGroup.add(rightPole)
        Scene.groundGroup.add(self.moveableLeftPlatform)
        Scene.groundGroup.add(self.moveableRightPlatform)
        Scene.groundGroup.add(topOfLeftPolePlatform)
        Scene.groundGroup.add(topOfRightPolePlatform)
        Scene.groundGroup.add(betweenDoorsPlatform)
        Scene.groundGroup.add(bottomGreenArea)
        Scene.groundGroup.add(jumpPlatformLeft)
        Scene.groundGroup.add(jumpPlatformRight)
        Scene.groundGroup.add(leftBluePlatform)
        Scene.groundGroup.add(rightRedPlatform)

        Scene.drawables.append(floor)
        Scene.drawables.append(ceiling)
        Scene.drawables.append(rightWall)
        Scene.drawables.append(leftWall)
        Scene.drawables.append(leftSidePlatform)
        Scene.drawables.append(rightSidePlatform)
        Scene.drawables.append(leftSidePlatformTop)
        Scene.drawables.append(rightSidePlatformTop)
        Scene.drawables.append(largeBottomMiddlePlatform)
        Scene.drawables.append(leftPole)
        Scene.drawables.append(rightPole)
        Scene.drawables.append(self.moveableLeftPlatform)
        Scene.drawables.append(self.moveableRightPlatform)
        Scene.drawables.append(topOfLeftPolePlatform)
        Scene.drawables.append(topOfRightPolePlatform)
        Scene.drawables.append(betweenDoorsPlatform)
        Scene.drawables.append(bottomGreenArea)
        Scene.drawables.append(jumpPlatformLeft)
        Scene.drawables.append(jumpPlatformRight)
        Scene.drawables.append(leftBluePlatform)
        Scene.drawables.append(rightRedPlatform)



