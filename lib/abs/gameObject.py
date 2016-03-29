##############################################################################
# gameObject.py
##############################################################################
# Base class for objects that appear on a scene.
##############################################################################
# 09/09 GoshDarnGames.com
##############################################################################

import pygame

class GameObject:
   
   def __init__(self,scene,pos,width,height,colour=(255,255,255)):
      self.scene = scene
      self.rect = pygame.Rect(pos[0],pos[1],width,height)
      self.colour = colour
      
   def render(self):
      
      pygame.draw.rect(self.scene.gameEngine.screen,self.colour,self.rect)
      
   def update(self):
      pass