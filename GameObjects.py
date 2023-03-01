
import pygame, sys
from pygame.locals import *
import random
import sys
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

class Ground(Drawable, pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        print(x)
        print(y)
        self.body = scene.Scene.world.CreateStaticBody(position=(x, y),
        fixtures = b2FixtureDef(shape=b2PolygonShape(box=(w/2, h/2)), friction=1000, density=1000))
        self.image = pygame.Surface((w*b2w, h*b2w))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position.x * b2w, 768 - self.body.position.y * b2w

    def draw(self, screen):
        screen.blit(self.image, self.body.position * b2w)
        #pygame.draw.rect(screen, (0, 255, 0), self.rect);
        # for fixture in self.body.fixtures:
        #     fixture.shape.draw(self.body, fixture)

class Player(DrawableUpdateable, pygame.sprite.DirtySprite):
    def __init__(self, player):
        super().__init__()
        pygame.sprite.DirtySprite.__init__(self)
        self.player = player
        color = (255, 0, 0) if player == 1 else (0, 0, 255)

        self.movingRight = False
        self.movingLeft = False

        self.body = scene.Scene.world.CreateDynamicBody(position=(1, 5 if player == 1 else 7))
        shape=b2CircleShape(radius=.25)
        fixDef = b2FixtureDef(shape=shape, friction=0.9, restitution=.1, density=1)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2
        d=.25*b2w*2
        self.image = pygame.Surface((d,d), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        #self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, color, self.rect.center, .25*b2w)

    def update(self, delta_time):
        # for ground in scene.Scene.groundGroup:
        #     print("Player: " + str(self.rect.x) + ", " + str(self.rect.y))
        #     print("Ground: " + str(ground.rect.x) + ", " + str(ground.rect.y))
        self.rect.center = self.body.position[0] * b2w, 760 - self.body.position[1] * b2w
        collided = pygame.sprite.spritecollide(self, scene.Scene.groundGroup, False)

        print(collided)

        for event in eg.Engine.events:
            #if event.type == pg.MOUSEMOTION:
            #    print(pg.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                if event.key == (pygame.K_w if self.player == 1 else pygame.K_UP):
                    #if len(collided) > 0:
                    self.body.ApplyForceToCenter(b2Vec2(0, 50), True)
                if event.key == (pygame.K_a if self.player == 1 else pygame.K_LEFT):
                    self.movingLeft = True
                if event.key == (pygame.K_d if self.player == 1 else pygame.K_RIGHT):
                    self.movingRight = True

            if event.type == pygame.KEYUP:
                if event.key == (pygame.K_a if self.player == 1 else pygame.K_LEFT):
                    self.movingLeft = False
                    self.body.linearVelocity = b2Vec2(0, self.body.linearVelocity.y)
                if event.key == (pygame.K_d if self.player == 1 else pygame.K_RIGHT):
                    self.movingRight = False
                    self.body.linearVelocity = b2Vec2(0, self.body.linearVelocity.y)

            if self.movingRight:
                self.body.linearVelocity = b2Vec2(200 * delta_time, self.body.linearVelocity.y)
            if self.movingLeft:
                self.body.linearVelocity = b2Vec2(-200 * delta_time, self.body.linearVelocity.y)


    def draw(self, screen):
        screen.blit(self.image, self.body.position * b2w)


    
        
    
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

