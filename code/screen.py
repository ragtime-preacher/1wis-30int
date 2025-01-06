# Screen
#   contains functionality to display information about a given class.

from curses import window
from Character import Character
from surface import Surface

# thanks, ChatGPT
from abc import ABC, abstractmethod

class Screen (ABC) :
    
    def __init__(self):
        # Screen.surface
        #   a two-dimensional array to store lines and columns - coordinates, 
        #       in other words. conveniently, the (y, x) ordering used by
        #       curses interfaces perfectly with the two-dimensional array
        #       system. Maybe that's why they started using it in the first
        #       place?? sei la mano
        self.surface = Surface([[]])
        pass


        # render ()
        #   stores the needed character data in the surface attribute.
        #       this needs to be implimented individually by the 
        #       child classes.
    @abstractmethod
    def render (self, source: Character) -> None:
        pass

        # draw ()
        #   This is the real point of the parent class - to inherit 
        #       the drawing functionality to the child classes.
    def draw (self, dest: window) -> None:
        for i_row in range(len(self.surface.data)):
            dest.addstr(i_row, 0, self.surface.data[i_row])

class TestScreen(Screen):
    def __init__(self):
        self.surface = Surface ([[]])

    def render (self):
        self.surface = Surface ([
            "123",
            "456",
            "789"
        ])