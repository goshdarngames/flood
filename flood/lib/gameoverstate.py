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

TIME_TAKEN_TXT_Y = 140
TIME_TAKEN_COLOR = NUM_CLICKS_COLOR

NEW_HIGH_SCORE_TXT_Y = 190
NEW_HIGH_SCORE_COLOR = (0,255,0)

OLD_SCORE_TXT_Y = 230
OLD_SCORE_COLOR = (0,0,255)

OLD_TIME_TXT_Y = 270
OLD_TIME_COLOR = OLD_SCORE_COLOR

NEW_BEST_TIME_TXT_Y = NEW_HIGH_SCORE_TXT_Y
NEW_BEST_TIME_COLOR = NEW_HIGH_SCORE_COLOR

ANY_KEY_TXT_Y = 440
ANY_KEY_COLOR = (255,0,255)

HIGH_SCORE_FILE = os.path.join("data","high_score.txt")

#GLOBAL SCREEN SIZE FOR TEXT CENTERING
SCREEN_SIZE = None

#character used to split the score from the time
SCORE_DELIMITER = ":"

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
   
   def __init__(self,model,click_count,fps,frames_elapsed):
      
      State.__init__(self,model)
      
      screen_width = self.model.screen_size[0]
      self.fps = fps
      
      #read old best time and score
      old_score_and_time = self._read_high_score()
      old_high_score = int(old_score_and_time[0])
      old_best_time = int(old_score_and_time[1])
      
      #check for new best score
      new_high_score = False  
      if click_count < old_high_score:
         new_high_score = True
         self._write_high_score(click_count,frames_elapsed)
         
      #check for new best time
      new_best_time = False
      if frames_elapsed < old_best_time and not new_high_score:
         new_best_time = True
         self._write_high_score(old_high_score,frames_elapsed)
         
      
      
      #game over text      
      self.game_objects.append(TextObject("GAME OVER",GAME_OVER_TXT_Y,
                                         GAME_OVER_COLOR,screen_width))
      
      #how many clicks
      num_clicks_text = "It took you "+str(click_count)+" clicks"
      
      self.game_objects.append(TextObject(num_clicks_text,NUM_CLICKS_TXT_Y,
                                          NUM_CLICKS_COLOR,screen_width))
                                          
      #time taken
      time_taken_text = "Your time: "+self._frames_to_time(frames_elapsed)
      
      self.game_objects.append(TextObject(time_taken_text,TIME_TAKEN_TXT_Y,
                                          TIME_TAKEN_COLOR,screen_width))
      
      
      #new high score
      if new_high_score:                               
         self.game_objects.append(TextObject("!!!NEW HIGH SCORE!!!",
                                             NEW_HIGH_SCORE_TXT_Y,
                                             NEW_HIGH_SCORE_COLOR,
                                             screen_width))
                                             
      if new_best_time:
         self.game_objects.append(TextObject("!!!NEW BEST TIME!!!",
                                             NEW_BEST_TIME_TXT_Y,
                                             NEW_BEST_TIME_COLOR,
                                             screen_width))
      
      #old high score
      old_score_text = ""
      
      if new_high_score:
         old_score_text = "Old high score: "+str(old_high_score)+" clicks"
      else:
         old_score_text = "High score: "+str(old_high_score)+" clicks"
      
      
      self.game_objects.append(TextObject(old_score_text,OLD_SCORE_TXT_Y,
                                          OLD_SCORE_COLOR, screen_width))
                                          
                                          
      #old time taken
      old_time_taken_text = ""
      
      if not new_high_score:
      
         if new_best_time:
            old_time_taken_text = "Old best time: "+\
                                          self._frames_to_time(old_best_time)
         else:
            old_time_taken_text = "Best time: "+\
                                           self._frames_to_time(old_best_time)
      
      
      self.game_objects.append(TextObject(old_time_taken_text,
                                          OLD_TIME_TXT_Y,
                                          OLD_TIME_COLOR, screen_width))
      
      #press any key      
      self.game_objects.append(TextObject("Press any key to continue.",
                                          ANY_KEY_TXT_Y,ANY_KEY_COLOR,
                                          screen_width))
      
   #--------------------------------------------------------------------------
   
   def notify(self,event):
      
      if isinstance(event,KeyboardEvent):
      
         if event.key == pygame.K_ESCAPE:
            self.model.system_event_manager.post(QuitEvent())
         
         from gamestate import GameState
         self.model.change_state(GameState(self.model,self.fps))
         
   #--------------------------------------------------------------------------
   
   def _frames_to_time(self,frames):
      minutes = frames/(self.fps*60)
      seconds = (frames%(self.fps*60))/float(self.fps)
      return "%02d:%05.2f" % (minutes,seconds)
         
   #--------------------------------------------------------------------------
   
   def _read_high_score(self):
   
      high_score_file = open(HIGH_SCORE_FILE,'r')
      high_score = []
       
      try:
         for line in high_score_file:
            high_score = line.split(SCORE_DELIMITER)
      except ValueError:
         pass
         
      high_score_file.close()
         
      return high_score  
      
   #--------------------------------------------------------------------------
   
   def _write_high_score(self,new_high_score,new_best_time):
   
      high_score_file = open(HIGH_SCORE_FILE,'w')
      
      high_score_file.write(str(new_high_score)+SCORE_DELIMITER+\
                            str(new_best_time))
      
      high_score_file.close()