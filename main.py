from Engine import Engine
import pygame, sys

# Creates a new instance of the Engine class and starts the main game loop
# When the loop is finished it will end pygames gracefully
if __name__ == '__main__':
    e = Engine()
    e.loop()
    pygame.quit()