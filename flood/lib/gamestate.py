##############################################################################
# gamestate.py
##############################################################################
# Classes related to the game play state.
##############################################################################
# 12/12 GoshDarnGames
##############################################################################

import pygame
import math
import random

from engine.abs.gameobject import GameObject
from engine.abs.state import State
from engine.abs.events import *
from engine.systemevents import *

from gameoverstate import GameOverState

##############################################################################
# CONSTANTS
##############################################################################

#number of squares in the puzzle.  Should be a square number that divides
#into the screen_size without remainder
NUM_SQUARES = 144

COLORS = [(255,0,0),(255,255,0),(255,0,255),
          (0,255,0), (0,0,255), (0,255,255)]

##############################################################################
# GAME EVENTS
##############################################################################

class SquareClicked(Event):
   """
   Generated by the game event manager when the player clicks on a square.
   """
   
   def __init__(self,square_idx):
      """
      square_idx - index of the square clicked
      """
      self.square_idx = square_idx
      
class GridUpdated(Event):
   """
   Generated by the grid when the user clicks on an edge square and all
   connected squares have been changed.
   """
   pass
      
##############################################################################
# GAME EVENTS - MANAGER AND LISTENER CLASSES
##############################################################################

class GameEventManager(EventManager):
   pass

class GameEventListener(Listener):
   pass

##############################################################################
# GAME OBJECTS - GRID
##############################################################################

class Grid(GameObject,GameEventListener):
   
   def __init__(self,game_event_manager,square_size):
      GameEventListener.__init__(self,game_event_manager)
      
      self.game_event_manager = game_event_manager
      
      self.squares = []
      self._populate_squares()
      self.square_size = square_size
      
      #stores which squares have been visited by the recursive algorithms
      #for detecting neighbours and such so that they don't recurse infinitely
      self._visited = []
      
   #--------------------------------------------------------------------------
      
   def _populate_squares(self):
   
      self.squares = []
   
      for i in range(NUM_SQUARES):
         self.squares.append(random.choice(COLORS))
         
   #--------------------------------------------------------------------------
         
   def render(self,screen):
      
      for i in range(len(self.squares)):
         #work out the x/y of the rect in order to place squares in a grid
         left = self.square_size*(i%int(math.sqrt(NUM_SQUARES)))
         top = self.square_size*(i/int(math.sqrt(NUM_SQUARES)))
         
         to_draw = pygame.Rect(left, top,self.square_size,self.square_size)
         
         pygame.draw.rect(screen,self.squares[i],to_draw)
         
   #--------------------------------------------------------------------------
   
   def notify(self,event):
      if isinstance(event,SquareClicked):
         
         #check if the clicked square is a neighbour of top-left block
         if event.square_idx in self._get_edge_squares():
         
            #change all attached blocks to the clicked colour
            for attached_idx in self._get_attached():
               self.squares[attached_idx] = self.squares[event.square_idx]
               
            self.game_event_manager.post(GridUpdated())
         
   #--------------------------------------------------------------------------
   
   def _get_attached(self):
      """
      Returns a list of squares attached to the top-left square.
      """
      
      self._visited = []
      
      return self._recurse_attached(0)
      
   #--------------------------------------------------------------------------
      
   def _recurse_attached(self,idx):
      """
      Traverses all squares attached to 'idx' and returns a list of squares
      connected to it.
      """
   
      self._visited.append(idx)
   
      attached = [idx]
      
      for n in self._get_neighbours(idx):
      
         if n in self._visited:
            continue
            
         if self.squares[n] == self.squares[idx]:
            attached+= self._recurse_attached(n)
            
      return attached
   
   #--------------------------------------------------------------------------
   
   def _get_edge_squares(self):
      """
      Returns a list of squares that surround the block of squares connected
      to the top-left corner.
      """
      
      #cells already visited
      self._visited = []
      
      #list of neighbours to be returned
      return self._recurse_edge_squares(0)
      
   #--------------------------------------------------------------------------
   
   def _recurse_edge_squares(self,idx):
      """
      Used to traverse all squares connected to 'idx' and return a list of
      squares around the edge of that block.
      """
      
      self._visited.append(idx)
      
      neighbours = self._get_neighbours(idx)
      
      edge_squares = []
      
      for n in neighbours:
      
         if n in self._visited:
            continue
      
         if(self.squares[n] == self.squares[idx]):
            edge_squares += self._recurse_edge_squares(n) 
         else:
            edge_squares.append(n)
            
      return edge_squares          
      
   #--------------------------------------------------------------------------
      
   def _get_neighbours(self,idx):
      """
      Returns a list of squares that are next to a given block.
      """
      
      neighbours = []
      
      #east
      if (idx+1)%int(math.sqrt(NUM_SQUARES)) is not 0:
         neighbours.append(idx+1)
      
      #west
      if (idx-1)%int(math.sqrt(NUM_SQUARES)) is not \
                                             int(math.sqrt(NUM_SQUARES))-1:
         neighbours.append(idx-1)
      
      #north
      if idx-int(math.sqrt(NUM_SQUARES)) in range(len(self.squares)):
         neighbours.append(idx-int(math.sqrt(NUM_SQUARES)))
      
      #south
      if idx+int(math.sqrt(NUM_SQUARES)) in range(len(self.squares)):
         neighbours.append(idx+int(math.sqrt(NUM_SQUARES)))
      
      return neighbours
         
      

##############################################################################
# GAME STATE CLASS
##############################################################################

class GameState(State,SystemEventListener,GameEventListener):

   def __init__(self,model,fps):
      State.__init__(self,model)
      
      #create game event manager and register self as listener
      self.game_event_manager = GameEventManager()
      GameEventListener.__init__(self,self.game_event_manager)
      
      self.screen_size = self.model.screen_size
      
      self.fps = fps
      self.frames_elapsed = 0
      
      #set the square_size so all squares will fit in the playing field
      self.square_size = self.screen_size[0]/math.sqrt(NUM_SQUARES)
      self.grid = Grid(self.game_event_manager,self.square_size)
      
      #check for the highly unlikely situation where all squares are the
      #same      
      while(self._check_win()):
         self.grid = Grid(self.game_event_manager,self.square_size)   
      
      self.game_objects.append(self.grid)
      
      self.click_count = 0    
      
   #--------------------------------------------------------------------------
   
   def notify(self,event):
      if isinstance(event,KeyboardEvent):
         if event.key == pygame.K_ESCAPE:
            self.model.system_event_manager.post(QuitEvent())
            
      if isinstance(event,MouseButtonEvent):
         if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.game_event_manager.post(
                              SquareClicked(self._pos_to_grid_idx(event.pos)))
                              
      if isinstance(event,GridUpdated):
         self.click_count += 1
         
         if self._check_win():
            self.model.change_state(GameOverState(self.model,
                                                  self.click_count,
                                                  self.fps,
                                                  self.frames_elapsed))
                                                  
      if isinstance(event,TickEvent):
         self.frames_elapsed+=1
            
   #--------------------------------------------------------------------------
   
   def _pos_to_grid_idx(self,pos):
      """
      For some reason I decided it would be a great idea to store the squares
      in a 1 dimensional array instead of a 2d array... here is the function
      to convert screen (x,y) into a list index for the grid.
      """
      x = int(math.floor(pos[0]/self.square_size))
      y = int(math.floor(pos[1]/self.square_size))
      return x+(y*int(math.sqrt(NUM_SQUARES)))
      
   #--------------------------------------------------------------------------
   
   def _check_win(self):
      """
      Here's when my 1d array design finally pays off!
      """
      return len(set(self.grid.squares)) is 1
               
               
   
