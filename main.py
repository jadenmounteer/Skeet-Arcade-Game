"""
File: skeet.py
Original Author: Br. Burton
Completed By: Jaden Mounteer
This program implements an awesome version of skeet.
"""
import arcade
import math
import random

# These are Global constants to use throughout the game
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500

RIFLE_WIDTH = 100
RIFLE_HEIGHT = 20
RIFLE_COLOR = arcade.color.DARK_RED

BULLET_RADIUS = 3
BULLET_COLOR = arcade.color.BLACK_OLIVE
BULLET_SPEED = 10

TARGET_RADIUS = 20
TARGET_COLOR = arcade.color.CARROT_ORANGE
TARGET_SAFE_COLOR = arcade.color.AIR_FORCE_BLUE
TARGET_SAFE_RADIUS = 15

class Point():
    """
    This class represents a point in the game.
    """

    def __init__(self):
        """
        Sets up the initial conditions of the point.
        :param x: float
        :param x: float
        """
        self.x = 0
        self.y = 0

class Velocity():
    """
    This class represents the velocity of an object.
    """

    def __init__(self):
        """
        Sets up the initial conditions of the velocity.
        :param dx: float
        :param dy: float
        """
        self.dx = 0
        self.dy = 0


# TODO: Fix this class so that all of the flying classes inherit the right things.
class Flying_Object():
    """
    This class represents a flying object in the game.
    """
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.radius = 0.0
        self.alive = True


    def advance(self):
        """
        Makes the object move if it is alive.
        :return: None
        """
        if self.alive:
            self.center.x += self.velocity.dx
            self.center.y += self.velocity.dy


    def draw(self):
        """
        Draws the object.
        :return: None
        """
        pass

    def is_off_screen(self, screen_width, screen_height):
        """
        Checks to see if the object is off the screen.
        :param screen_width:
        :param screen_height:
        :return: Boolean
        """
        if self.center.x < 0.0 or self.center.x > screen_width:
            return True
        if self.center.y < 0.0 or self.center.y > SCREEN_HEIGHT:
            return False

# TODO: Finish the Bullet class.
class Bullet(Flying_Object):
    """
    A flying bullet. Child class of the Flying_object class.
    Overrides the center, velocity, and radius member variables.
    Adds a draw() method to the class.
    Adds a fire() method to the class.
    Adds an advance() method to the class.
    """
    def __init__(self):
        """
        Initializes the bullet.
        """
        super().__init__()
        self.radius = BULLET_RADIUS

        # Initializes a bullet starting at (25, 25)
        self.center.x = 25
        self.center.y = 25

        # Sounds
        self.bullet_sound = arcade.load_sound("pepSound1.ogg")

    def draw(self):
        """
        Draws a bullet to the screen.
        Renders it aas a filled-in circle.
        :return: None
        """
        texture = arcade.load_texture("bullet.png")
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius*2, self.radius*2, texture)
        #arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, arcade.color.GOLD)

    def fire(self, angle: float):
        """
        Fires the bullet.
        :param angle:
        :return:
        """
        # Angles the bullet horizontally.
        self.velocity.dx = math.cos(math.radians(angle)) * BULLET_SPEED
        # Angles the bullet vertically.
        self.velocity.dy = math.sin(math.radians(angle)) * BULLET_SPEED
        self.alive = True

    #def advance(self):
        """
        Moves the bullet through the air.
        Travels at a 10 pixels/frame at the angle at which
        it was fired.
        :return: None
        """
        #self.center.x += self.velocity.dx
        #self.center.y += self.velocity.dy



# TODO: Finish the Target class.
class Target(Flying_Object):
    """
    A flying standard target. Child class of the Flying_object class.
    Overrides the center, velocity, and radius attributes.
    Adds an alive member variable.
    Adds a draw() method to the class.
    Adds a hit() method to the class.
    """
    def __init__(self):
        super().__init__()

        # Target sound
        self.target_sound = arcade.load_sound("Bomb+1.mp3")

        # Select random location for the Flying object class
        self.center.x = 0.0
        self.center.y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT)



    def advance(self):
        """
        Makes the target move.
        :return: None
        """
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    def is_off_screen(self, screen_width, screen_height):
        """
        Checks to see if the bullet is off the screen.
        :param screen_width:
        :param screen_height:
        :return: Boolean
        """
        pass


    def draw(self):
        """
        Draws a target to the screen.
        The initial position of the target is anywhere along the top
        half of the left side of the screen.
        :return:
        """
        #arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, self.color)

    def hit(self):
        """
        Represents the target getting hit.
        Kills the standard target in one hit.
        and returns an integer representing the points scored for that hit.
        :return: int
        """
        self.alive = False
        return 1

# TODO: Create a Strong Target class that inherits from the Target class.

# TODO: Create a Safe Target class that inherits from the Target class.

class Rifle:
    """
    The rifle is a rectangle that tracks the mouse.
    """
    def __init__(self):
        self.center = Point() # This was originally set to (25,25)
        self.center.x = 0
        self.center.y = 0

        self.angle = 45

    def draw(self):
        arcade.draw_rectangle_filled(self.center.x, self.center.y, RIFLE_WIDTH, RIFLE_HEIGHT, RIFLE_COLOR, self.angle)


class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    It assumes the following classes exist:
        Rifle
        Target (and it's sub-classes)
        Point
        Velocity
        Bullet
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class, but mostly
    you shouldn't have to. There are a few sections that you
    must add code to.
    """

    def __init__(self, width, height, title):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height, title)

        self.rifle = Rifle()
        self.score = 0

        # Creates a list for the bullets.
        self.bullets = []

        # Creates a list for the targets
        self.targets = []

        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # draw each object
        self.rifle.draw()

        # Iterates through the bullets and draws them.
        for bullet in self.bullets:
            bullet.draw()

        # Iterates through the targets and draws them.
        for target in self.targets:
            target.draw()

        self.draw_score()

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.NAVY_BLUE)

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_collisions()
        self.check_off_screen()

        # decide if we should start a target by giving a 1 in 50 chance.
        if random.randint(1, 50) == 1:
            self.create_target()

        # Iterates through the bullets and tells them to advance.
        for bullet in self.bullets:
            bullet.advance()

        # TODO: Iterate through your targets and tell them to advance
        # Iterates through the targets and tells them to advance.
        for target in self.targets:
            target.advance()

    def create_target(self):
        """
        Creates a new target of a random type and adds it to the list.
        :return:
        """

        # TODO: Decide what type of target to create and append it to the list
        # So far, I just have one target object; the Standard Target.
        target = Target()
        self.targets.append(target)




    def check_collisions(self):
        """
        Checks to see if bullets have hit targets.
        Updates scores and removes dead items.
        :return:
        """

        # NOTE: This assumes you named your targets list "targets"

        for bullet in self.bullets:
            for target in self.targets:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and target.alive:
                    too_close = bullet.radius + target.radius

                    if (abs(bullet.center.x - target.center.x) < too_close and
                                abs(bullet.center.y - target.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False
                        self.score += target.hit()

                        # We will wait to remove the dead objects until after we
                        # finish going through the list

        # Now, check for anything that is dead, and remove it
        self.cleanup_zombies()

    def cleanup_zombies(self):
        """
        Removes any dead bullets or targets from the list.
        :return:
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for target in self.targets:
            if not target.alive:
                self.targets.remove(target)

    def check_off_screen(self):
        """
        Checks to see if bullets or targets have left the screen
        and if so, removes them from their lists.
        :return:
        """
        for bullet in self.bullets:
            if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.bullets.remove(bullet)

        for target in self.targets:
            if target.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.targets.remove(target)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # set the rifle angle in degrees
        self.rifle.angle = self._get_angle_degrees(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # Fire!
        angle = self._get_angle_degrees(x, y)

        bullet = Bullet()
        bullet.fire(angle)

        self.bullets.append(bullet)

    def _get_angle_degrees(self, x, y):
        """
        Gets the value of an angle (in degrees) defined
        by the provided x and y.
        Note: This could be a static method, but we haven't
        discussed them yet...
        """
        # get the angle in radians
        angle_radians = math.atan2(y, x)

        # convert to degrees
        angle_degrees = math.degrees(angle_radians)

        return angle_degrees

# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, "Awesome Skeet")
arcade.run()
