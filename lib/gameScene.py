##############################################################################
# gameScene.py
##############################################################################
# Contains the classes used to render and explore the maze.
##############################################################################
# 04/12 GoshDarnGames.com
##############################################################################

import pygame
import os

from abs.scene import Scene
from abs.gameObject import GameObject

##############################################################################
# GLOBAL VARIABLES
##############################################################################

GRID_WIDTH = 30
GRID_HEIGHT = 30

CELL_WIDTH = 20
CELL_HEIGHT = CELL_WIDTH

MAN_COLOUR = (255,0,0)
MAN_SPEED = 8

WALL_COLOUR = (255,255,255)
GOAL_COLOUR = (0,255,0)


##############################################################################
# CLASSES
##############################################################################

##############################################################################
# Game Scene
##############################################################################

class GameScene(Scene):
   
   def __init__(self,gameEngine):
      Scene.__init__(self,gameEngine) 
      
      self.man = None
      self.goal = None
      self.walls = []
      
      self.level = 1
      self.__loadLevel()
      
   #-------------------------------------------------------------------------- 
      
   def render(self):
      self.man.render()
      self.goal.render()
      
      for wall in self.walls:
         wall.render()
      
   #--------------------------------------------------------------------------
      
   def update(self):
         
      self.man.update()
         
   #--------------------------------------------------------------------------
   
   def nextLevel(self):
      """
      Loads the next level.
      """
      
      self.level+=1
      self.__loadLevel()
      
   #--------------------------------------------------------------------------
   
   def __loadLevel(self):
   
      self.walls = []
      
      file_name = os.path.join("data","levels","%03d"%self.level)
      
      #try to open the level file.  If it doesn't load go to game over
      try:
         f = open(file_name)
      except IOError:
         self.gameEngine.gameOver()
         return
         
      x=y=0
      
      #traverse the file adding objects as encountered
      while 1:
         row = f.readline()
         
         if not row:
            break
          
         x = 0   
         for col in row:
         
            if col == 'S':
               self.man = Man(self,(x,y))
            if col == 'G':
               self.goal = Goal(self,(x,y))
            if col == 'W':
               self.walls.append(Wall(self,(x,y)))
            
            x += CELL_WIDTH
         
         y += CELL_HEIGHT

   
##############################################################################
# Man
##############################################################################

class Man(GameObject):
   
   def __init__(self,scene,pos):
      GameObject.__init__(self,scene,pos,CELL_WIDTH,CELL_HEIGHT,MAN_COLOUR)
      
      self.start_pos = pos
      
      #direction to move
      self.direction = (0,0)
      
      #flag indicating whether the man is moving
      self.moving = False
      
   #--------------------------------------------------------------------------
      
   def update(self):
      
      #test for keypress if the man is not already moving
      if self.moving is False:
         events = self.scene.gameEngine.events
      
         for event in events:
            if event.type == pygame.KEYDOWN:
            
               #test for 'R' key.  Resets the man in case he's stuck
               if event.key == pygame.K_r:
                  self.__reset()
                  
            
               #test each of the arrow keys
               if event.key == pygame.K_RIGHT:
                  self.moving = True
                  self.direction = (1,0)
                  
               if event.key == pygame.K_LEFT:
                  self.moving = True
                  self.direction = (-1,0)
                  
               if event.key == pygame.K_UP:
                  self.moving = True
                  self.direction = (0,-1)
                  
               if event.key == pygame.K_DOWN:
                  self.moving = True
                  self.direction = (0,1)
                  
      #move the man, if necessary
      if self.moving is True:
         self.rect.left += self.direction[0]*MAN_SPEED
         self.rect.top += self.direction[1]*MAN_SPEED 
         
      #test if the man is outside the bounds of the screen
      if self.rect.left >= GRID_WIDTH*CELL_WIDTH or  \
         self.rect.top >= GRID_WIDTH*CELL_HEIGHT or \
         self.rect.right <=0 or \
         self.rect.bottom <= 0 :
         
         self.__reset()
         
      #test to see if we're touching the goal
      if self.rect.colliderect(self.scene.goal.rect):
         self.scene.nextLevel()
         
      #test for wall collisions
      if self.moving is True:
         for wall in self.scene.walls:
            if self.rect.colliderect(wall.rect):
               self.moving = False
               
               #move the man to the edge of the wall
               if self.direction == (1,0):
                  self.rect.right = wall.rect.left
               if self.direction == (-1,0):
                  self.rect.left = wall.rect.right
               if self.direction == (0,1):
                  self.rect.bottom = wall.rect.top
               if self.direction == (0,-1):
                  self.rect.top = wall.rect.bottom
                  
   #--------------------------------------------------------------------------
      
   def __reset(self):
      """
      Returns the man to his starting position.
      """
         
      self.rect.left = self.start_pos[0]
      self.rect.top = self.start_pos[1]
      self.moving = False 
         
         
##############################################################################
# Wall
##############################################################################

class Wall(GameObject):
   
   def __init__(self,scene,pos):
      GameObject.__init__(self,scene,pos,CELL_WIDTH,CELL_HEIGHT,WALL_COLOUR)
      
##############################################################################
# Goal
##############################################################################

class Goal(GameObject):
   
   def __init__(self,scene,pos):
      GameObject.__init__(self,scene,pos,CELL_WIDTH,CELL_HEIGHT,GOAL_COLOUR)  
      