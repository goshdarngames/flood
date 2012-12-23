##############################################################################
# gameoverstate.py
##############################################################################
# The state the user is brought to when they complete the game.
##############################################################################
# 12/12 flembobs
##############################################################################

import pygame
import os

from engine.abs.gameobject import GameObject
from engine.abs.state import State
from engine.systemevents import *

##############################################################################
# CONSTANTS
##############################################################################

GAME_OVER_TXT_Y = 20
GAME_OVER_COLOR = (255,0,0)

NUM_CLICKS_TXT_Y = 100
NUM_CLICKS_COLOR = (255,255,255)

NEW_HIGH_SCORE_TXT_Y = 150
NEW_HIGH_SCORE_COLOR = (0,255,0)

OLD_SCORE_TXT_Y = 200
OLD_SCORE_COLOR = (0,0,255)

ANY_KEY_TXT_Y = 240
ANY_KEY_COLOR = (255,0,255)

HIGH_SCORE_FILE = os.path.join("data","high_score.txt")

#GLOBAL SCREEN SIZE FOR TEXT CENTERING
SCREEN_SIZE = None

##############################################################################
# GAME OBJECT - TEXT
##############################################################################

class TextObject(GameObject):
   
   def __init__(self,text,y, color,screen_width):
      """
      text  - text to be displayed
      y     - y to be drawn at.  The text will be centered
      color - color to draw the text
      """
      
      self.screen_width = screen_width
   
      self.surf = pygame.font.SysFont("courier",24,True).\
                                                     render(text,True,(color))
      self.pos = (self._center_text(self.surf),y)
      
   def render(self,screen):
      
      screen.blit(self.surf,self.pos)
      
   def _center_text(self,surf):
      """
      Returns the x coordinate this surf should be drawn at to be centered
      on screen.
      """
      x = self.screen_width/2
      x -= surf.get_width()/2
      return x   

##############################################################################
# GAME OVER STATE
##############################################################################

class GameOverState(State,SystemEventListener):
   
   def __init__(self,model,click_count):
      
      State.__init__(self,model)
      
      screen_width = self.model.screen_size[0]
      
      old_high_score = self._read_high_score()
      
      new_high_score = False
      if click_count < old_high_score:
         new_high_score = True
         self._write_high_score(click_count)
         
      
      
      #game over text      
      self.game_objects.append(TextObject("GAME OVER",GAME_OVER_TXT_Y,
                                         GAME_OVER_COLOR,screen_width))
      
      #how many clicks
      num_clicks_text = "It took you "+str(click_count)+" clicks!"
      
      self.game_objects.append(TextObject(num_clicks_text,NUM_CLICKS_TXT_Y,
                                          NUM_CLICKS_COLOR,screen_width))
      
      
      #new high score
      if new_high_score:                               
         self.game_objects.append(TextObject("!!!NEW HIGH SCORE!!!",
                                             NEW_HIGH_SCORE_TXT_Y,
                                             NEW_HIGH_SCORE_COLOR,
                                             screen_width))
      
      #old high score
      old_score_text = ""
      
      if new_high_score:
         old_score_text = "Old high score: "+str(old_high_score)+" clicks!"
      else:
         old_score_text = "High score: "+str(old_high_score)+" clicks!"
      
      
      self.game_objects.append(TextObject(old_score_text,OLD_SCORE_TXT_Y,
                                          OLD_SCORE_COLOR, screen_width))
      
      #press any key      
      self.game_objects.append(TextObject("Press any key to continue.",
                                          ANY_KEY_TXT_Y,ANY_KEY_COLOR,
                                          screen_width))
      
   #--------------------------------------------------------------------------
   
   def notify(self,event):
      
      if isinstance(event,KeyboardEvent):
         
         from gamestate import GameState
         self.model.change_state(GameState(self.model))
         
   #--------------------------------------------------------------------------
   
   def _read_high_score(self):
   
      high_score_file = open(HIGH_SCORE_FILE,'r')
      high_score = 144
       
      try:
         for line in high_score_file:
            high_score = int(line)
      except ValueError:
         pass
         
      high_score_file.close()
         
      return high_score  
      
   #--------------------------------------------------------------------------
   
   def _write_high_score(self,new_high_score):
   
      high_score_file = open(HIGH_SCORE_FILE,'w')
      
      high_score_file.write(str(new_high_score))
      
      high_score_file.close()