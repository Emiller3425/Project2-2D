
import pygame, sys
from pygame import mixer
from pygame.locals import *
import random
import sys
import json
import math
import copy
from Box2D import *
from Box2D.b2 import *
import Engine as eg
import Scene as scene

b2w = 100
w2b = 1/100

class Drawable:
    def init(self):
        pass

    def draw(self, delta_time):
        pass


class Updateable:
    def init(self):
        pass

    def update(self, screen):
        pass


class DrawableUpdateable(Drawable, Updateable):
    def init(self):
        super().init()


class Updater(Updateable):
    def __init__(self, time_step, velocity, position):
        super().__init__()
        self.world = scene.Scene.world
        self.time_step = time_step
        self.velocity = velocity
        self.position = position
    def update(self, delta_time):
        self.world.Step(self.time_step, self.velocity, self.position)
        self.world.ClearForces()

class GroundButton(Drawable, pygame.sprite.Sprite):
    def __init__(self, x, y, platform, state):
        super().__init__()
        self.x = x
        self.y = y
        self.w = .2
        self.h = .2
        self.type = type
        self.color = (0,0,0)
        self.platfrom = platform
        self.state = state
        self.body = scene.Scene.world.CreateStaticBody(position=(x, y),
        fixtures = b2FixtureDef(shape=b2PolygonShape(box=(self.w/2, self.h/2)), friction=1000, density=1000))
        self.image = pygame.Surface((self.w*b2w,self.h*b2w))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = x * b2w, 768 - y * b2w

    def pressed(self):
        if self.state == False:
            self.state = True
            mixer.Sound('buttonPress.mp3').play()
        scene.Scene.buttonPress(eg.Engine.current_scene, self.platfrom)

    def unpressed(self):
        if self.state == True:
            self.state = False
            scene.Scene.buttonUnpress(eg.Engine.current_scene, self.platfrom)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Door(Drawable, pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.x = x
        self.y = y
        self.w = .5
        self.h = 1
        self.type = type
        if type == 1:
            self.image = pygame.image.load('betterRed.png')
        else:
            self.image = pygame.image.load('betterBlue.png')
        #self.body = scene.Scene.world.CreateStaticBody(position=(x, y),
        #fixtures = b2FixtureDef(shape=b2PolygonShape(box=(self.w/2, self.h/2)), friction=1000, density=1000))

        self.rect = self.image.get_rect()
        self.rect.center = x * b2w, 768 - y * b2w

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Stallagtite(Drawable, pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pygame.image.load('stalagtites.png')
        self.rect = self.image.get_rect()
        self.rect.center = x * b2w, 768 - y * b2w
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Ground(Drawable, pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, type):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.type = type

        if type == 1:
            #red water
            self.image = pygame.transform.scale(scene.Scene.sprites[0], (w*b2w, h*b2w))
        elif type == 2:
            #blue water
            self.image = pygame.transform.scale(scene.Scene.sprites[2], (w*b2w, h*b2w))
        elif type == 3:
            #green water
            self.image = pygame.transform.scale(scene.Scene.sprites[1], (w*b2w, h*b2w))
        else:
            #ground
            self.image = pygame.transform.scale(scene.Scene.sprites[3], (w*b2w, h*b2w))

        self.body = scene.Scene.world.CreateStaticBody(position=(self.x, self.y),
        fixtures = b2FixtureDef(shape=b2PolygonShape(box=(w/2, h/2)), friction=1000, density=1000))

        #self.image = pygame.transform.scale(pygame.image.load('sprite.png'), (w*b2w, h*b2w))
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position.x * b2w, 768 - self.body.position.y * b2w

    def move(self, new_x):
        self.x += new_x
        self.body.position = (self.x, self.y)
        self.rect.center = self.x * b2w, 768 - self.body.position.y * b2w

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Player(DrawableUpdateable, pygame.sprite.DirtySprite):
    def __init__(self, player):
        super().__init__()
        pygame.sprite.DirtySprite.__init__(self)
        self.player = player

        self.facingRight = True
        self.movingRight = False
        self.movingLeft = False

        self.atFinalDoor = False

        self.activeButton = None

        self.d = .25 * b2w * 2
        self.body = scene.Scene.world.CreateDynamicBody(position=(1 if player == 1 else 9, .5))
        shape = b2CircleShape(radius=.25/2)
        fixDef = b2FixtureDef(shape=shape, friction=0.9, restitution=.1, density=4)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2
        if player == 1:
            self.image = pygame.transform.scale(scene.Scene.sprites[33], (self.d, self.d))
        else:
            self.image = pygame.transform.scale(scene.Scene.sprites[5], (self.d, self.d))
        self.rect = self.image.get_rect()

    def reset(self):
        mixer.Sound('Splash.mp3').play()
        self.body.position = (1 if self.player == 1 else 9, .5)

    def update(self, delta_time):
        self.rect.center = self.body.position[0] * b2w, 758 - self.body.position[1] * b2w
        collided = pygame.sprite.spritecollide(self, scene.Scene.groundGroup, False)
        movableRightCollision = pygame.sprite.spritecollide(self, scene.Scene.moveableRightGroup, False)
        movableLeftCollision = pygame.sprite.spritecollide(self, scene.Scene.moveableLeftGroup, False)
        doorCollision = pygame.sprite.spritecollide(self, scene.Scene.doorGroup, False)
        buttonCollision = pygame.sprite.spritecollide(self, scene.Scene.buttonGroup, False)

        if len(collided) > 0:
            if collided[0].type == 1 and not (self.player == 1):
                scene.Scene.reset_players(eg.Engine.current_scene)
            elif collided[0].type == 2 and not (self.player == 2):
                scene.Scene.reset_players(eg.Engine.current_scene)
            elif collided[0].type == 3:
                scene.Scene.reset_players(eg.Engine.current_scene)


        if len(doorCollision) > 0:
            if doorCollision[0].type == self.player:
                self.atFinalDoor = True
            else:
                self.atFinalDoor = False

        if len(buttonCollision) > 0:
            self.activeButton = buttonCollision[0]
            buttonCollision[0].pressed()
        else:
            if self.activeButton:
                self.activeButton.unpressed()
                self.activeButton = None

        scene.Scene.check_win(eg.Engine.current_scene)

        for event in eg.Engine.events:
            if event.type == pygame.KEYDOWN:
                if event.key == (pygame.K_w if self.player == 1 else pygame.K_UP):
                    if len(collided) > 0 or len(buttonCollision) or len(movableRightCollision) or len(movableLeftCollision) > 0:
                        self.body.ApplyForceToCenter(b2Vec2(0, 70), True)
                        self.jump()
                if event.key == (pygame.K_a if self.player == 1 else pygame.K_LEFT):
                    self.movingLeft = True
                    self.facingRight = False
                if event.key == (pygame.K_d if self.player == 1 else pygame.K_RIGHT):
                    self.movingRight = True
                    self.facingRight = True

            if event.type == pygame.KEYUP:
                if event.key == (pygame.K_a if self.player == 1 else pygame.K_LEFT):
                    self.movingLeft = False
                    if self.player == 1:
                        self.image = pygame.transform.flip(pygame.transform.scale(scene.Scene.sprites[33], (self.d, self.d)), True, False)
                    else:
                        self.image = pygame.transform.flip(pygame.transform.scale(scene.Scene.sprites[5], (self.d, self.d)), True, False)
                    self.body.linearVelocity = b2Vec2(0.0, self.body.linearVelocity.y)
                if event.key == (pygame.K_d if self.player == 1 else pygame.K_RIGHT):
                    self.movingRight = False
                    if self.player == 1:
                        self.image = pygame.transform.scale(scene.Scene.sprites[33], (self.d, self.d))
                    else:
                        self.image = pygame.transform.scale(scene.Scene.sprites[5], (self.d, self.d))
                    self.body.linearVelocity = b2Vec2(0.0, self.body.linearVelocity.y)

        if self.movingRight:
            self.body.linearVelocity = b2Vec2(150 * delta_time, self.body.linearVelocity.y)
            self.walkingRight()
        elif self.movingLeft:
            self.body.linearVelocity = b2Vec2(-150 * delta_time, self.body.linearVelocity.y)
            self.walkingLeft()
        else:
            self.body.linearVelocity = b2Vec2(0.0, self.body.linearVelocity.y)

    def walkingRight(self):
        if self.player == 1:
            for i in range(0, 2):
                self.image = pygame.transform.scale(scene.Scene.sprites[33 + i], (self.d, self.d))
        else:
            for i in range(0, 2):
                self.image = pygame.transform.scale(scene.Scene.sprites[5 + i], (self.d, self.d))
    
    def walkingLeft(self):
        if self.player == 1:
            for i in range(0, 2):
                self.image = pygame.transform.flip(pygame.transform.scale(scene.Scene.sprites[33 + i], (self.d, self.d)), True, False)
        else:
            for i in range(0, 2):
                self.image = pygame.transform.flip(pygame.transform.scale(scene.Scene.sprites[5 + i], (self.d, self.d)), True, False)
    
    def jump(self):
        if self.player == 1:
            if self.facingRight:
                self.image = pygame.transform.scale(scene.Scene.sprites[36], (self.d, self.d))
            else:
                self.image = pygame.transform.flip(pygame.transform.scale(scene.Scene.sprites[36], (self.d, self.d)), True, False)
        else:
            if self.facingRight:
                self.image = pygame.transform.scale(scene.Scene.sprites[8], (self.d, self.d))
            else:
                self.image = pygame.transform.flip(pygame.transform.scale(scene.Scene.sprites[8], (self.d, self.d)), True, False)


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    
# Reusable button object that can display a rectangle with text in it on the screen and exepts click events
class Button(Drawable):
    """ Initializes the sprite object and creates the surface used for collision detection and drawing to the screen

        Args:
            width: number of pixels wide the button is
            height: number of pixels tall the button is
            color: color the button
            screen: holds the scene for the game
            pos_x: the x position on the screen
            pos_y: the y position on the screen
            text: the text to display 
            text_color: the color of the text
            text_bg_color: the color behind the text
            font_name: the font to use for the text
            font_size: the size of the font
        """
    def __init__(self, height, width, color, screen, pos_x, pos_y, text, text_color, text_bg_color, font_name, font_size):
        self.height = height
        self.width = width
        self.color = color
        self.screen = screen
        self.x = pos_x
        self.y = pos_y
        font = pygame.font.SysFont(font_name, font_size)
        self.text = font.render(text, True, text_color, text_bg_color)

    def check_click(self, cursor):
        """ Checks if the mouse click event was within the area of the button

        Args:
            cursor: the cordinates of the pygame.mouse object
        """
        if ((cursor[0] >= self.x and cursor[0] < (self.x + self.width))
         and (cursor[1] >= self.y and cursor[1] < (self.y + self.height))):
            return True
        else:
            return False

    def fire_event(self, event):
        """ Fires the event that the button is used for 

        Args:
            event: the event corresponding to the button click
        """
        event

    def draw(self):
        """ Draws a rect at the position passed in at the constructor and blits the text at the same postion on the screen """
        pygame.draw.rect(self.screen, self.color, [self.x, self.y, self.width, self.height])
        self.screen.blit(self.text, (self.x + 2, self.y))

