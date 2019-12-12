"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

Adam Kadhim ak779, Calvin Johnson clj78
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def create_ship(self):
        """
        """
        self._x_ship = GAME_WIDTH//2
        self._y_ship = SHIP_BOTTOM
        self._ship = Ship(self._x_ship, self._y_ship,'ship.png')

    def initialize_aliens(self,x,y):
        """
        This helper creates the alien objects the first time only.
        """
        self._aliens = []
        self._alien_y = y
        sources = ['alien1.png','alien2.png','alien3.png']

        #Specifies which image file is
        source_num = 2

        #Uses nested for loops to create each alien object in 2d list
        for row_of_aliens in range(ALIEN_ROWS):
            source = sources[source_num]
            self._alien_x = x
            sub_alien = []

            for row_alien in range(ALIENS_IN_ROW):
                to_add = Alien(self._alien_x,self._alien_y,source)
                sub_alien.append(to_add)
                self._alien_x += ALIEN_H_SEP + ALIEN_WIDTH
                if row_alien == ALIENS_IN_ROW-1 and row_of_aliens % 2 == 0:
                    source_num -= 1
                    self._alien_y -= ALIEN_V_SEP + ALIEN_HEIGHT
                    self._aliens.append(sub_alien)
                elif row_alien == ALIENS_IN_ROW-1:
                    self._alien_y -= ALIEN_V_SEP + ALIEN_HEIGHT
                    self._aliens.append(sub_alien)

    def new_aliens(self,x,y):
        """
        This helper methods removes the previous Alien objects and recreates
        the new frame of them, moved from their previous position.

        Paramater x: x position of first alien to draw in new position of wave
        Precondition: x is an int

        Paramater y: y position of first alien to draw in new position of wave
        Precondition: y is an int
        """
        self._aliens = []
        self._baseline_alien_x = x
        self._baseline_alien_y = y
        self._alien_y = y
        sources = ['alien1.png','alien2.png','alien3.png']

        #Specifies which image file is
        source_num = 2

        #Uses nested for loops to create each alien object in 2d list
        for row_of_aliens in range(ALIEN_ROWS):
            source = sources[source_num]
            self._alien_x = x
            sub_alien = []

            for row_alien in range(ALIENS_IN_ROW):
                to_add = Alien(self._alien_x,self._alien_y,source)
                sub_alien.append(to_add)
                self._alien_x += ALIEN_H_SEP + ALIEN_WIDTH
                if row_alien == ALIENS_IN_ROW-1 and row_of_aliens % 2 == 0:
                    source_num -= 1
                    self._alien_y -= ALIEN_V_SEP + ALIEN_HEIGHT
                    self._aliens.append(sub_alien)
                elif row_alien == ALIENS_IN_ROW-1:
                    self._alien_y -= ALIEN_V_SEP + ALIEN_HEIGHT
                    self._aliens.append(sub_alien)

    def move_aliens_right(self):
        """
        Helper function to update that moves the wave of aliens in the right
        direction. Resets attribute time back to 0 as well.
        """
        right_x = self._baseline_alien_x + ALIEN_H_WALK
        self.new_aliens(right_x, self._baseline_alien_y)
        self._time = 0

    def move_aliens_left(self):
        """
        Helper function to update that moves the wave of aliens in the left
        direction.
        """
        left_x = self._baseline_alien_x - ALIEN_H_WALK
        self.new_aliens(left_x, self._baseline_alien_y)
        self._time = 0

    def move_aliens_down(self,x):
        """
        Helper function to update that moves the wave of aliens in the down
        direction.

        Paramater x:
        Precondition:
        """
        down_y = self._baseline_alien_y - ALIEN_V_WALK
        self.new_aliens(x, down_y)
        self._time = 0

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes the class. Draws ships and aliens.
        """
        self._time = 0
        self._direction = None

        #Create the Alien objects
        self._baseline_alien_x = ALIEN_H_SEP + ALIEN_WIDTH
        self._baseline_alien_y = GAME_HEIGHT - ALIEN_CEILING
        self.initialize_aliens(self._baseline_alien_x, self._baseline_alien_y)

        #Create the ship object and defense line to draw
        self.create_ship()
        self._line = GPath(points = [0, DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],
                linewidth  = 1, linecolor = 'black')

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,time_since):
        """
        Updates the frame of the program to move ships, aleins and bolts.

        Paramater input:
        Precondition:

        Paramater time_since:
        Precondition:
        """
        self._time += time_since
        movement_differential = 0
        if input.is_key_down('right'):
            movement_differential += SHIP_MOVEMENT
        if input.is_key_down('left'):
            movement_differential -= SHIP_MOVEMENT

        #makes sure wont make ship go off screen before changing location of it
        if (self._x_ship + movement_differential) >(GAME_WIDTH - SHIP_WIDTH//2):
            self._x_ship = GAME_WIDTH - (SHIP_WIDTH//2)
        elif (self._x_ship + movement_differential) < (SHIP_WIDTH//2):
            self._x_ship = SHIP_WIDTH//2
        else:
            self._x_ship += movement_differential

        #New ship object with updated location
        self._ship = Ship(self._x_ship,self._y_ship,'ship.png')

        counter = 0
        right_edge = self._alien_x + ALIEN_H_SEP + ALIEN_WIDTH//2
        left_edge = self._baseline_alien_x - ALIEN_H_SEP - ALIEN_WIDTH//2
        if right_edge > GAME_WIDTH:  #right border hit
            self._direction = 'left'
            counter +=1
        if left_edge < 0:
            self._direction = 'right'
            counter +=1

        #Aliens in new location
        if self._time > ALIEN_SPEED:         #time to move the wave (reanimate)
            if self._direction =='right' or self._direction == None:
                if counter != 0:
                    self.move_aliens_down(self._baseline_alien_x)
                self.move_aliens_right()
                counter=0
            elif self._direction =='left':
                if counter != 0:
                    self.move_aliens_down(self._baseline_alien_x)
                self.move_aliens_left()
                counter = 0

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draws the ships, aliens, defense line, and bolts.

        Paramater view:
        Precondition:
        """
        #assert preconditions?
        for row in self._aliens:
            for alienz in row:
                alienz.draw(view)

        self._ship.draw(view)
        self._line.draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
