
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

class Drawable:
    def init(self):
        pass

    def draw(self, delta_time):
        raise NotImplementedError


class Updateable:
    def init(self):
        pass

    def update(self, screen):
        raise NotImplementedError


class DrawableUpdateable(Drawable, Updateable):
    def init(self):
        super().init()


class Updater(Updateable):
    def __init__(self, world, time_step, velocity, position):
        super().__init__()
        self.world = world
        self.time_step = time_step
        self.velocity = velocity
        self.position = position
    def update(self, delta_time):
        self.world.Step(self.time_step, self.velocity, self.position)
        self.world.ClearForces()

class Ground(Drawable, pygame.sprite.Sprite):
    def __init__(self, world, x, y, w, h):
        super().__init__()
        self.body = world.CreateStaticBody(position=(x, y), shapes=b2PolygonShape(box=(w, h)))
        self.image = pygame.Surface((2*w*100, 2*h*100))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position.x * 100, 768 - self.body.position.y * 100

    def draw(self, screen):
        screen.blit(self.image, self.body.position * 100)

class Player(DrawableUpdateable, pygame.sprite.DirtySprite):
    def __init__(self, world, player):
        super().__init__()
        self.world = world
        self.player = player

        self.body = world.CreateDynamicBody(position=(5, 5))
        shape=b2CircleShape(radius=.25)
        fixDef = b2FixtureDef(shape=shape, friction=0.3, restitution=.5, density=.5)
        box = self.body.CreateFixture(fixDef)
        self.dirty = 2
        d=.25*100*2
        self.image = pygame.Surface((d,d), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        #self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image,(0, 101, 164) , self.rect.center, .25*100)

    def update(self, delta_time):
        self.rect.center = self.body.position[0] * 100, 768 - self.body.position[1] * 100
        collided = pygame.sprite.spritecollide(self, scene.Scene.groundGroup, False)
        for event in eg.Engine.events:
            #if event.type == pg.MOUSEMOTION:
            #    print(pg.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if len(collided) > 0:
                        self.body.ApplyForceToCenter( (0, 100), True)
                elif event.key == pygame.K_a:
                    self.body.ApplyForceToCenter( (-100, 0), True)
                elif event.key == pygame.K_d:
                    self.body.ApplyForceToCenter( (100, 0), True)

    def draw(self, screen):
        if self.dirty > 0:
            screen.blit(self.image, self.body.position * 100)
        else:
            self.dirty -= 1


    
        
    
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

