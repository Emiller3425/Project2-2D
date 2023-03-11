
import pygame
import sys
from pygame.locals import *
from pygame import mixer
import sys
from Box2D import *
from GameObjects import *
import Engine as eg

# Creates the pygames window and holds all game objects


class Scene:

    pygame.mixer.init()
    mixer.music.load('Cave.mp3')
    mixer.music.play(-1)

    updateables = []
    drawables = []
    sprites = []

    groundGroup = pygame.sprite.Group()
    moveableLeftGroup = pygame.sprite.Group()
    moveableRightGroup = pygame.sprite.Group()
    doorGroup = pygame.sprite.Group()
    buttonGroup = pygame.sprite.Group()
    StallagtiteGroup = pygame.sprite.Group()

    gravity = b2Vec2(0, -10.0)
    world = b2World(gravity, doSleep=False)

    rightPressed = False
    leftPressed = False

    def __init__(self):

        self.time_step = 1.0 / eg.Engine.frame_rate
        self.vel_iters, self.pos_iters = 6, 2
        self.add_sprites()
        self.add_objects()

    def reset_players(self):
        self.player1.reset()
        self.player2.reset()

    def check_win(self):
        if self.player1.atFinalDoor and self.player2.atFinalDoor:
            button = Button(200, 1000, Color(50,50,50), eg.Engine.screen, 80, 80,
                            'Made by: Josh Fletcher and Ethan Miller', (0, 0, 0), (50,50,50), 'timesnewroman', 50)
            button.draw()

    def add_sprites(self):
        sprite_sheet = pygame.image.load('spritesheet.png').convert_alpha()
        sprite_width, sprite_height = 32, 32
        for row in range(sprite_sheet.get_height() // sprite_height):
            for col in range(sprite_sheet.get_width() // sprite_width):
                x = col * sprite_width
                y = row * sprite_height
                sprite = sprite_sheet.subsurface(
                    pygame.Rect(x, y, sprite_width, sprite_height))
                Scene.sprites.append(sprite)

    def add_objects(self):
        """Creates an instance of all objects used in the game and adds them to the correct lists"""
        Scene.updateables.append(
            Updater(self.time_step, self.vel_iters, self.pos_iters))

        self.player1 = Player(1)
        self.player2 = Player(2)

        player1Door = Door(4, 3, 1)
        player2Door = Door(6, 3, 2)

        leftBottomButton = GroundButton(.55, 3.6, 2, False)
        rightBottomButton = GroundButton(9.5, 3.6, 1, False)

        leftTopButton = GroundButton(3, 6.1, 2, False)
        rightTopButton = GroundButton(7, 6.1, 1, False)

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

        self.addStallagtites()
        self.add_platforms()

    def buttonPress(self, type):
        if type == 1 and self.leftPressed == False:
            for moveable in Scene.moveableRightGroup:
                moveable.move(-2)
            self.leftPressed = True
        elif type == 2 and self.rightPressed == False:
            for moveable in Scene.moveableLeftGroup:
                moveable.move(2)
            self.rightPressed = True

    def buttonUnpress(self, type):
        if type == 1 and self.leftPressed == True:
            for moveable in Scene.moveableRightGroup:
                moveable.move(2)
            self.leftPressed = False
        elif type == 2 and self.rightPressed == True:
            for moveable in Scene.moveableLeftGroup:
                moveable.move(-2)
            self.rightPressed = False

    def addStallagtites(self):
        for i in range(0, 21):
            stal = Stallagtite(0.50 * i, 7.0, 0.59, 0.100)
            Scene.drawables.append(stal)
            Scene.updateables.append(stal)

    def add_platforms(self):
        # cieling
        for i in range(0, 34):
            ground = Ground(i * 0.31, 7.6, .32, .32, 0)
            Scene.groundGroup.add(ground)
            Scene.drawables.append(ground)
        # floor
        for i in range(0, 34):
            ground = Ground(i * 0.31, 0, .32, .32, 0)
            Scene.groundGroup.add(ground)
            Scene.drawables.append(ground)
        # right wall
        for i in range(0, 26):
            ground = Ground(10.1, i * 0.31, .32, .32, 0)
            Scene.groundGroup.add(ground)
            Scene.drawables.append(ground)
        # left wall
        for i in range(0, 26):
            ground = Ground(0, i * 0.31, .32, .32, 0)
            Scene.groundGroup.add(ground)
            Scene.drawables.append(ground)
        # leftside platforms
        for i in range(1, 5):
            ground = Ground(i * 0.31, 1.5, .32, .32, 0)
            Scene.groundGroup.add(ground)
            Scene.drawables.append(ground)
        # rightside platforms
        for i in range(1, 5):
            ground = Ground(10.1 - i * 0.31, 1.5, .32, .32, 0)
            Scene.groundGroup.add(ground)
            Scene.drawables.append(ground)
        # leftside top platform
        for i in range(1, 5):
            ground = Ground(i * 0.31, 3.5, .32, .32, 0)
            Scene.groundGroup.add(ground)
            Scene.drawables.append(ground)
        # rightside top platform
        for i in range(1, 5):
            ground = Ground(10.1 - i * 0.31, 3.5, .32, .32, 0)
            Scene.groundGroup.add(ground)
            Scene.drawables.append(ground)
        # large bottom middle platform
        for i in range(0, 21):
            ground = Ground(1.92 + i * 0.31, 2.5, .32, .32, 0)
            Scene.groundGroup.add(ground)
            Scene.drawables.append(ground)
        # left pole
        for i in range(0, 12):
            ground = Ground(3, 2.5 + i * 0.31, .32, .32, 0)
            Scene.groundGroup.add(ground)
            Scene.drawables.append(ground)
        # right pole
        for i in range(0, 12):
            ground = Ground(7, 2.5 + i * 0.31, .32, .32, 0)
            Scene.groundGroup.add(ground)
            Scene.drawables.append(ground)
        # left pole platform
        for i in range(0, 5):
            ground = Ground(2.36 + i * 0.31, 6, .32, .32, 0)
            Scene.groundGroup.add(ground)
            Scene.drawables.append(ground)
        # right pole platform
        for i in range(0, 5):
            ground = Ground(6.36 + i * 0.31, 6, .32, .32, 0)
            Scene.groundGroup.add(ground)
            Scene.drawables.append(ground)
        # between doors platform
        for i in range(0, 3):
            ground = Ground(4.68 + i * 0.31, 4, .32, .32, 0)
            Scene.groundGroup.add(ground)
            Scene.drawables.append(ground)
        # green area
        for i in range(0, 15):
            ground = Ground(2.82 + i * 0.31, 0.02, .32, .32, 3)
            Scene.groundGroup.add(ground)
            Scene.drawables.append(ground)
        # jump platform left
        for i in range(0, 4):
            ground = Ground(3.14 + i * 0.31, 0.8, .32, .32, 0)
            Scene.groundGroup.add(ground)
            Scene.drawables.append(ground)
        # jump platform right
        for i in range(0, 4):
            ground = Ground(6 + i * 0.31, 0.8, .32, .32, 0)
            Scene.groundGroup.add(ground)
            Scene.drawables.append(ground)
        # blue platform
        for i in range(0, 4):
            ground = Ground(1.75 + i * 0.31, 2.51, .32, .32, 2)
            Scene.groundGroup.add(ground)
            Scene.drawables.append(ground)
        # red platform
        for i in range(0, 4):
            ground = Ground(7.32 + i * 0.31, 2.51, .32, .32, 1)
            Scene.groundGroup.add(ground)
            Scene.drawables.append(ground)
        # left button platform
        for i in range(0, 3):
            ground = Ground(3.7 + i * 0.31, 5, .32, .32, 0)
            Scene.moveableRightGroup.add(ground)
            Scene.drawables.append(ground)
        # right button platform
        for i in range(0, 3):
            ground = Ground(5.7 + i * 0.31, 5, .32, .32, 0)
            Scene.moveableLeftGroup.add(ground)
            Scene.drawables.append(ground)
