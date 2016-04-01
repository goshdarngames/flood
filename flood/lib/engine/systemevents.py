##############################################################################
# systemevents.py
##############################################################################
# Definitions of all system events monitored by the game engine's main
# event manager.
##############################################################################
# 06/12 - GoshDarnGames
##############################################################################

from abs.events import *

##############################################################################
# EVENTS
##############################################################################

class TickEvent(Event):
   """
   Generated by the CPU Spinner when a game loop occurs
   """
   pass
   
class QuitEvent(Event):
   """
   Generated by the model when the user tries to quit the game.
   """
   pass
   
class KeyboardEvent(Event):
   """
   Generated by the pygame event monitor when the user presses or releases a 
   key.
   """   
   
   def __init__(self,type,key):
      """
      type - pygame.KEYUP or pygame.KEYDOWN
      key - which key e.g. pygame.K_ESCAPE
      """ 
      
      self.type = type
      self.key = key
      
class MouseButtonEvent(Event):
   """
   Generated by the pygame event monitor when the user presses or releases
   a mouse button.
   """
   
   def __init__(self,type,button,pos):
      """
      type - pygame.MOUSEBUTTONUP or pygame.MOUSEBUTTONDOWN
      button - which mouse button was pressed
      pos - position of the mouse at time of event
      """
      
      self.type = type                            
      self.button = button
      self.pos = pos
      
class MouseMotionEvent(Event):
   """
   Generated by the pygame event monitor when the user moves the mouse.
   """
   
   def __init__(self,pos,rel,buttons):
      """
      pos - new position of the mouse
      rel - position relative to the old position
      buttons - which buttons are being pressed
      """
            
      self.pos = pos
      self.rel = rel
      self.buttons = buttons
      
class ModelUpdated(Event):
   """
   Generated by the model after it processes a tick event.
   """
   
   def __init__(self,game_objects):
      """
      game_objects - list of Game Objects that are tracked by the model.  
                     These will be drawn in this order by the default 
                     pygame view.
      """
   
      self.game_objects = game_objects

##############################################################################
# LISTENER
##############################################################################

class SystemEventListener(Listener):
   pass

##############################################################################
# EVENTS MANAGER
##############################################################################

class SystemEventManager(EventManager):
   pass