import pygame

class Centipede:

    """
    Represents the centipede in game.
    Uses instance variables for position, speed, size, and colour as there is only one centipede, and if more are added in the future,
    they could be different shapes, sizes, colours and speeds.
    These are private to prevent external modification and enforce encapsulation.
    """
    
    def __init__(self, x, y, size, speed, colour):
        self.__x = x
        self.__y = y
        self.__speed_x = speed
        self.__size = size
        self.__colour = colour
        
    def __str__(self):
        return f"Centipede at ({self.__x}, {self.__y}), Colour: {self.__colour}"

    # draws centipede on screen as a rectangle
    def draw(self, display):
        pygame.draw.rect(display, self.__colour, [self.__x, self.__y, self.__size, self.__size])

    # moves centipede horizontally only, and at a set speed
    def move(self):
        self.__x = self.__x + self.__speed_x
        return self.__x
        
    # relocates centipede to its origanl starting position (which is passed in through dims)
    def relocate(self, dims):
        self.__x = dims[0]
        self.__y = dims[1]

    # handles edge collisions, reverses direction of centipede if it hits the canvas edges and moves centipede down vertically
    def collide(self, dims):
        edge = dims[0] - self.__size # so centipede remains fully in the bounds of the canvas when bouncing
        if self.__x < 0:
            self.__speed_x = self.__speed_x*-1 # reverse direction
            self.__y += 15 # vertical movement. Spped of 15 is chosen as it is slow enough that the centipede can be shot with the dart but fast enough that it is challenging to do so
        if self.__x > edge:
            self.__speed_x = self.__speed_x*-1
            self.__y += 15

    # passes in canvas dimensions (display_dims) and cent starting pos (cent_dims) to check if halfway point is passed by centipede
    # then return the centipede to starting position if True
    def halfway(self, display_dims, cent_dims): 
        halfway_point = display_dims[1]//2 - self.__size
        if self.__y >= halfway_point:
            self.relocate(cent_dims)
            
    # --- getters ---
    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y
    
    def get_size(self):
        return self.__size