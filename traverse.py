##############################################################################
# traverse.py
##############################################################################
# Main game engine for the Traverse project.
##############################################################################
# 04/12 GoshDarnGames.com
##############################################################################

import pygame
import os 

from lib.gameScene import GameScene
from lib.gameOver  import GameOverScene 

##############################################################################   
# GLOBAL VARIABLES
##############################################################################

PROJECT_NAME = "Traverse"

BG_COLOUR = (0,0,0)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

##############################################################################
# Game Engine class
##############################################################################

class GameEngine():
                                                                              
   ###########################################################################
   # INIT
   ###########################################################################
   
   def __init__(self):
      
      #initialize pygame
      os.environ["SDL_VIDEO_CENTERED"] = "1"
      pygame.init()
      
      #set up the display
      pygame.display.set_caption(PROJECT_NAME)
      self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

      self.clock = pygame.time.Clock()

      self.events = []
      
      self.newGame()
    
   ###########################################################################
   # MAIN GAME LOOP
   ###########################################################################
      
   def loop(self):
      while True:

         self.__getEvents()

         self.clock.tick(60)
         self.screen.fill(BG_COLOUR)
         
         self.scene.update()
         self.scene.render()

         pygame.display.flip()

         if self.__checkQuit():
            break
      
   ###########################################################################
   # FUNCTIONS
   ###########################################################################
   
   def newGame(self):
      self.scene = GameScene(self)
      
   def gameOver(self):
      self.scene = GameOverScene(self)
   
   def __checkQuit(self):

      for e in self.events:
         if e.type == pygame.QUIT:
            return True
         if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            return True

      return False

   def __getEvents(self):
      self.events = pygame.event.get()

##############################################################################
# Main Execution Logic
##############################################################################

gE = GameEngine()
gE.loop()
pygame.quit()