import pygame

class Shooter:
    """
    Represents the player-controlled shooter.
    Instance variables are private to encapsulate position, size, colour, and speed.
    """
    def __init__(self, x, y, size, colour, speed):
        self.__size = size
        self.__x = x
        self.__y = y
        self.__colour = colour
        self.__speed_x = speed
    
    def __str__(self):
        return f"Shooter at ({self.__x}, {self.__y}), Colour: {self.__colour}"
    
    # draws shooter as a rectangle
    def draw(self, display):
        pygame.draw.rect(display, self.__colour, [self.__x, self.__y, self.__size, self.__size])
    
    # moves shooter left if it is not beyond the canvas edge (0)
    def move_left(self):
        if self.__x > 0:
            self.__x = self.__x + self.__speed_x
        return self.__x
    
    # moves shooter right if it is not beyond the canvas edge (calculated using dims)
    def move_right(self, dims):
        edge = dims[0] - self.__size
        if self.__x < edge:
            self.__x = self.__x - self.__speed_x
        return self.__x
    
    # --- getters ---
    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y
    
    def get_size(self):
        return self.__size
    
    def get_speed(self):
        return self.__speed_x