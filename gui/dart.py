import pygame, random

class Dart:
    
    """
    Represents a dart fired by the shooter.
    Instance variables are private to encapsulate position, size, colour, speed, and active state.
    """
    
    def __init__(self, x, y, size, colour, speed):
        self.__active = False
        self.__size = size
        self.__colour = colour
        self.__x = x
        self.__y = y
        self.__speed = speed
        
    def __str__(self):
        return f"Dart at ({self.__x}, {self.__y}), Colour: {self.__colour}"
    
    # draws dart as a rectangle
    def draw(self, display):
        if not self.__active: # only draws if it is active
            return
        pygame.draw.rect(display, self.__colour, [self.__x, self.__y, self.__size, self.__size])
    
    # activates the dart if not already active
    def activate(self):
        if not self.__active:
            self.__active = True
            #print("Dart activated")
    
    # deactivates the dart if it is ctive
    def deactivate(self):
        if self.__active:
            self.__active = False
            #print("Dart deactivated")
    
    # sets dart position only if the dart is inactive, ensures the dart position is not altered mid flight 
    def set_position(self, new_position): # new_position passed in as a list of two integers 
        if not self.__active:
            self.__x = new_position[0]
            self.__y = new_position[1]

    # moves dart upwards if active, deactivates if it passes through the top of the canvas bounds
    def fire(self, dims):
        if self.__active:
            self.__y = self.__y - self.__speed
        if self.__y <= 0:
            self.deactivate()
    
    # --- getters ---
    def get_active(self):
        return self.__active
    
    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y
    
    def get_size(self):
        return self.__size
    