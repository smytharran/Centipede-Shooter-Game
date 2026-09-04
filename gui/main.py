    # --------- PSEUDOCODE ----------------------
'''
The description below is pseudocode of the flow of a typical pygame application
Import library
init pygame library
create display surface
setup for all features to be drawn
create timer

Run GAME LOOP until a certain condition fails:
    redraw background
    prepare all drawable elements
    respond to events
    update display
    update framerate

quit pygame
quit application
'''


import pygame
from centipede import Centipede
from shooter import Shooter
from dart import Dart

# ------------------- INIT PYGAME -----------------------------
pygame.init() # THIS IS REQUIRED

# ------------- SETTING UP PYGAME DISPLAY ---------------------
# store window width, height, display size
display_width = 400
display_height= 400
display_size = (display_width, display_height) # can be a tuple or a list
display = pygame.display.set_mode(display_size) 
dims_list = [display_width, display_height] # list of dimensions as some methods expect dims in format of [w, h]

# --------------color variable --------------------------------

black = (0, 0, 0) # dark background colour for good contrast against brightly coloured sprites

# setup of objects needed - initial position, size, colour, etc.


# Collision Check:
# Uses getters for x, y, and size, for both the dart and the centipede to get up to date location info.
# Checks if the two squares overlap/collide, if they do deactivate the dart and send the centipede back to the starting position
def collision_check(dart, cent, dimensions):
    if (dart.get_x() < cent.get_x() + cent.get_size() and dart.get_x() + dart.get_size() > cent.get_x() and
        dart.get_y() < cent.get_y() + cent.get_size() and dart.get_y() + dart.get_size() > cent.get_y()):
        print("Collision detected!")
        dart.deactivate()
        cent.relocate(dimensions)

# init centipede
cent_size = 30
cent_x = display_width - cent_size # start at the right edge of the canvas
cent_y = 0 # top of the canvas
cent_speed = -5 # negative means moving to the left towrads the x-axis centre (0), horizontal only
cent_colour = [160,32, 240] # purple agaisnt black looks nice :)
cent = Centipede(cent_x, cent_y, cent_size, cent_speed, cent_colour) # insantiaiting the Centipede class
cent_starting_pos = [cent_x, cent_y]

# init shooter
shooter_size = 30
shooter_x = (display_width - shooter_size)/2 # displays in middle of canvas 
shooter_y = display_height - shooter_size # displays at bottom of canvas
shooter_speed = -5 # negative used in speed to avoid duplicating sign handling, as must travel both directions
shooter_colour = [0, 255, 255] # cyan
shooter = Shooter(shooter_x, shooter_y, shooter_size, shooter_colour, shooter_speed)
shooter_moving_left = False # booleans used to allow for continous movement, initializing them for shooter here
shooter_moving_right = False

### ---- SETUP DART AREA -----
dart_size = 10 # smaller than shooter for visual congruance of dart being fired from shooter
dart_x = (shooter.get_x() + shooter.get_size() // 2) - (dart_size // 2)  #Compute initial dart position relative to shooter center (horizontal) top (vertical)
dart_y = shooter.get_y() - dart_size # Compute initial dart position relative to shooter top (vertical)
dart_colour = [255, 255, 0] # yellow
dart_speed = 6 
dart = Dart(dart_x, dart_y, dart_size, dart_colour, dart_speed)
dart_moving = False # initializing dart boolean for continous movement
dart_starting_pos = [dart_x, dart_y] # starting dart position in list format

# ---- SETUP EVENT LIST -----
class Event:

    def __init__(self, event):
        self.data = event
        self.next = None

class EventList:
    
    def __init__(self):
        self.head = None

    def add_data(self, data):
        # step 1: 
        ## create a new instance of the Node class
        ## store that instance in a local variable
        new_node_instance = Event(data)
        
        
        # step 2: 
        ## if there is no content in the head node:
        ## assign the head node the instance of the Node created above.
        ## terminate the method.
        if self.head is None:
            self.head = new_node_instance
            return        
        # step 3:
        ## assign a placeholder variable to the current node head.
        ## move through the list while the current Node points to another Node
        ## attach the instance of the Node to the end of the list.
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node_instance
    
    def display(self):
        if self.head is None:
            return
        
        current = self.head
        while current.next:
            print(current.data, end="-->")
            current = current.next
        print(current.data)

# init event list
link = EventList()

clock = pygame.time.Clock() # controls how freuqntly the while loop runs


# init a clock to control our time events, especially for speeding up/slowing down a game
clock = pygame.time.Clock()

# string representations 
print(cent)
print(shooter)
print(dart)

# ------------- GAME LOOP -------------------------------------
# variable to keep our game running
run_game = True
while run_game:
    display.fill(black) # fill background black

    # --- display drawable elements ---
    # 1. Draw starting positions
    shooter.draw(display)
    cent.draw(display)
    dart.draw(display)
    
    # 2. update/ move positions
    cent.move() # horizontal movement across canvas
    cent.collide(dims_list) # change directions when colliding with either canvas edge
    cent.halfway(dims_list, cent_starting_pos) # resets centipede to starting position if it passes the halfway point moving down the canvas

    # 3. check interactions
    collision_check(dart, cent, cent_starting_pos) # calls collision check function

    if dart.get_active() == False: # checking if the dart has been deactivted through hitting target or top of canvas, returns it to shooter 
        dart.set_position(dart_starting_pos)
        dart_moving = False # stops movement of dart

    # if shooter movement booleans become true (through arrows being pressed), call movement functions. Booleans allow for constant movement
    if shooter_moving_left: 
        shooter.move_left()
    if shooter_moving_right:
        shooter.move_right(dims_list) # dimensions needed for right edge of canvas, not needed for left edge (0)

    # dart upward motion when fired 
    if dart_moving: # checks if dart_moving boolean becomes true (through space bar being pressed)
        dart.activate() # activate dart
        dart.fire(display_size) # fires dart if dart is actived
        if dart.get_active() == False: # if dart is deactivated, set dart_moving boolean to False to stop movement
            dart_moving = False
    
    # keep dart position tracking centered above the shooter for the next shot
    dart_current_pos = [(shooter.get_x() + shooter.get_size() // 2) - (dart_size // 2), shooter.get_y() - dart_size]
    
    # --- respond to events --- 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # If the windows was closed via mouse press on 'x' at corner of window.
            link.add_data("Game terminated!") # log event to event list
            run_game = False
            
        elif event.type == pygame.KEYDOWN:
            # --- Shooter KEYDOWN (handles horizontal movement upon button presses) ---
            if event.key == pygame.K_LEFT:
                link.add_data("Shooter moving left!")
                shooter_moving_left = True # sets movement booleans to true
            if event.key == pygame.K_RIGHT:
                link.add_data("Shooter moving right!")
                shooter_moving_right = True
                
            # --- Dart KEYDOWN (position snapped to current shooter, then activated) ---
            if event.key == pygame.K_SPACE:
                link.add_data("Dart fired!")
                dart.set_position(dart_current_pos) # only works if not active (enforced in class)
                dart.activate()
                dart_moving = True
            elif event.key == pygame.K_z: # manual cancel key for dart
                link.add_data("Dart shot cancelled!")
                dart.deactivate()
                dart_moving = False
                
        elif event.type == pygame.KEYUP:
            # --- Shooter KEYUP (stops horizontal movement upon button release) ---
            if event.key == pygame.K_LEFT:
                link.add_data("Shooter stopped moving left.")
                shooter_moving_left = False
            if event.key == pygame.K_RIGHT:
                link.add_data("Shooter stopped moving right.")
                shooter_moving_right = False
                
    pygame.display.update() # update the display with drawable elements
    clock.tick(60) # reset the framerate, set to 60 FPS

pygame.quit() # quit pygame (deactivate modules, etc.)
link.display() # display the event list upon the game ending 
quit() # quit application
