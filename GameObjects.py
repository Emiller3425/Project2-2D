
import pygame, sys
from pygame.locals import *
import random
import sys
import math
import copy

# Reusable button object that can display a rectangle with text in it on the screen and exepts click events
class Button():
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