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

RIFLE_WIDTH = 20 
RIFLE_HEIGHT = 100 
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

class Flying_Object():
    """
    This class represents a flying object in the game.
    """
    def __init__(self):
        # Creates a member variable called center and sets it to the Point class.
        self.center = Point()
        # Creates a member variable called velocity and sets it to the Velocity class.
        self.velocity = Velocity()
        # Creates a member variable for radius.
        self.radius = 0.0
        # Creates a member variable called alive and sets it to True.
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
        # Uses Super() here in order to override some attributes of the Flying_object class, while keeping others.
        super().__init__()

        # Overrides the radius member variable and gives it the value of BULLET_RADIUS.
        self.radius = BULLET_RADIUS

        # Initializes the bullets at the corner of the screen, inside the barrel.
        self.center.x = 0
        self.center.y = 0

    def draw(self):
        """
        Draws a bullet to the screen.
        Renders it as a filled-in circle.
        :return: None
        """
        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, BULLET_COLOR)

    def fire(self, angle: float):
        """
        Fires the bullet.
        :param angle:
        :return:
        """
        # --- Inverted ---
        # Angles the bullet horizontally.
        #self.velocity.dx = math.cos(math.radians(angle)) * BULLET_SPEED
        # Angles the bullet vertically.
        #self.velocity.dy = math.sin(math.radians(angle)) * BULLET_SPEED
        # Changes the alive variable to True. Is this necessary?
        #self.alive = True

        # --- Correct ---
        # Angles the bullet horizontally.
        self.velocity.dx = math.sin(math.radians(angle)) * BULLET_SPEED
        # Angles the bullet vertically.
        self.velocity.dy = math.cos(math.radians(angle)) * BULLET_SPEED
        # Changes the alive variable to True. Is this necessary?
        self.alive = True

class Target(Flying_Object):
    """
    A flying standard target. Child class of the Flying_object class.
    Overrides the center, velocity, and radius attributes.
    Adds an alive member variable.
    Adds a draw() method to the class.
    Adds a hit() method to the class.
    """
    def __init__(self):
        # Uses Super() here in order to override some attributes of the Flying_object class, while keeping others.
        super().__init__()

        # Makes the target spawn anywhere in the left hand corner of the screen.
        self.center.x = 0.0
        self.center.y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - 50)

        # Declares a member variable for lives
        self.lives = 1

        # Overrides the radius member variable and gives it the value of TARGET_RADIUS.
        self.radius = TARGET_RADIUS

        # Overrides the velocity member variables and gives them the value of the standard target speed.
        self.velocity.dx = random.uniform(1, 5) # Gives the target a random horizontal velocity between 1 and 5 pixels/frame.
        self.velocity.dy = random.uniform(-2, 5) # Gives the target a random vertical velocity between -2 and 5 pixesl/frame.

    def draw(self):
        """
        Draws a target to the screen.
        The initial position of the target is anywhere along the top
        half of the left side of the screen.
        :return:
        """
        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, TARGET_COLOR)

    def hit(self):
        """
        Represents the target getting hit.
        Kills the standard target in one hit.
        and returns an integer representing the points scored for that hit.
        :return: int
        """
        print("A regular target was hit.")
        self.alive = False
        # Returns the number of points.
        return 1


class Strong_target(Target):
    """
    Represents a strong target.
    Inherits from the Target class.
    Moves more slowly than the others.
    Its horizontal velocity should be taken from the range 1 to 3.
    Its vertical velocity from the range -2 to +3.
    Takes 3 hits to destroy.
    1 point is awarded for each of the first two hits.
    5 points are awarded for the third hit that destroys the target.
    """
    def __init__(self):
        # Uses Super() here in order to override some attributes of the Target class, while keeping others.
        super().__init__()

        # Overrides the velocity member variables
        self.velocity.dx = random.uniform(1, 3)
        self.velocity.dy = random.uniform(-2, 3)

        # Declares a member variable for lives
        self.lives = 3

    def draw(self):
        """
        Draws a circle with a number inside of it.
        """
        arcade.draw_circle_outline(self.center.x, self.center.y, self.radius, arcade.color.PEACH)
        text_x = self.center.x - (self.radius / 2)
        text_y = self.center.y - (self.radius / 2)
        arcade.draw_text(repr(self.lives), text_x, text_y, TARGET_COLOR, font_size=20)

    def hit(self):
        """
        Represents the target getting hit.
        Kills the standard target in one hit.
        and returns an integer representing the points scored for that hit.
        :return: int
        """
        print("A strong target was hit")
        # Initiates the number of points at 0.
        points = 0

        # If the target has 3 lives
        if self.lives == 3:
            # Adds 1 point to points.
            points = 1
            # Decrements lives by 1
            self.lives -= 1

        # If the target has 2 lives.
        if self.lives == 2 and points == 0:
            # adds 1 point to points.
            points = 1
            # Decrements lives by 1
            self.lives -= 1

        # If the target has 1 life
        if self.lives == 1 and points == 0:
            # Adds 5 points to points
            points = 5
            # Decrements lives by 1.
            self.lives -= 1

        # If the target runs out of lives.
        if self.lives <= 0:
            self.alive = False

        # Returns the number of points.
        return points


class Safe_target(Target):
    """
    This class represents a safe target in the game.
    It is rendered as a square,
    It should not be hit.
    A penaly of 10 points is incurred if this target is hit.
    """
    def __init__(self):
        # Uses Super() here in order to override some attributes of the Target class, while keeping others.
        super().__init__()

    def draw(self):
        """
        Draws the target as a square to the screen.
        """
        arcade.draw_rectangle_filled(center_x=self.center.x, center_y=self.center.y, height=50, width=50, color=TARGET_SAFE_COLOR)

    def hit(self):
        """
        Represents the target getting hit.
        Kills the standard target in one hit.
        Takes away the 10 points from the player.
        :return: int
        """
        self.alive = False
        # Returns the number of points.
        return -10


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
        self.time = 75
        self.number_of_bullets_shot = 0
        self.number_of_targets_shot = 0
        self.number_of_points_scored = 0
        self.is_game_over = False
        self.game_started = False
        self.time_to_start_game = 30
        

        # Creates a list for the bullets.
        self.bullets = []

        # Creates a list for the targets
        self.targets = []

        arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()


        # ___Draws each object___
        

        # Iterates through the bullets and draws them.
        for bullet in self.bullets:
            bullet.draw()
        
        # Draws the rifle after the bullets so that the bullets are only visible once they leave
        # the barrel.
        self.rifle.draw()

        # Iterates through the targets and draws them.
        for target in self.targets:
            target.draw()

        # Draws the game instructions before the game begins.
        if self.game_started == False:
            self.draw_instructions()

        self.draw_score()

        # If the game is over, displays Game over to the screen.
        if self.is_game_over == True:
            self.draw_game_over()

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.NAVY_BLUE)

        # Draws the player's time.
        formatted_time = "{:.2f}".format(self.time)
        score_text = "Time Remaining: {}".format(formatted_time)
        start_x = 100
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.NAVY_BLUE)

    def draw_instructions(self):
        """
        Draws the words:
        Skeet Shoot
        A game made by Jaden Mounteer using Python 3.
        Shoot targets until time runs out.
        Don't shoot the squares!
        """
        title = "SKEET SHOOT"
        start_x = 10
        start_y = SCREEN_HEIGHT - 100
        arcade.draw_text(title, start_x=start_x, start_y=start_y, font_size=50, color=arcade.color.NAVY_BLUE)
        author_info = "A game made by Jaden Mounteer"
        start_x_2 = 10
        start_y_2 = SCREEN_HEIGHT - 130
        arcade.draw_text(author_info, start_x=start_x_2, start_y=start_y_2, font_size=25, color=arcade.color.NAVY_BLUE)
        more_author_info = "using Python 3"
        start_x_3 = 10
        start_y_3 = SCREEN_HEIGHT - 170
        arcade.draw_text(more_author_info, start_x=start_x_3, start_y=start_y_3, font_size=25, color=arcade.color.NAVY_BLUE)

        instructions1 = "Instructions:"
        start_x_4 = 10
        start_y_4 = SCREEN_HEIGHT / 2
        arcade.draw_text(instructions1, start_x=start_x_4, start_y=start_y_4, font_size=25,
                         color=arcade.color.NAVY_BLUE)
        instructions2 = "Left click to shoot. Use the mouse to aim."
        start_x_5 = 10
        start_y_5 = SCREEN_HEIGHT / 2 - 30
        arcade.draw_text(instructions2, start_x=start_x_5, start_y=start_y_5, font_size=25,
                         color=arcade.color.NAVY_BLUE)

        instructions3 = "Shoot as many targets as you can before"
        start_x_6 = 10
        start_y_6 = SCREEN_HEIGHT / 2 - 60
        arcade.draw_text(instructions3, start_x=start_x_6, start_y=start_y_6, font_size=25,
                         color=arcade.color.NAVY_BLUE)

        instructions4 = "time runs out."
        start_x_7 = 10
        start_y_7 = SCREEN_HEIGHT / 2 - 90
        arcade.draw_text(instructions4, start_x=start_x_7, start_y=start_y_7, font_size=25,
                         color=arcade.color.NAVY_BLUE)

        instructions4 = "Don't shoot the squares!"
        start_x_8 = 10
        start_y_8 = SCREEN_HEIGHT / 2 - 120
        arcade.draw_text(instructions4, start_x=start_x_8, start_y=start_y_8, font_size=25,
                         color=arcade.color.NAVY_BLUE)


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

        # Iterates through the targets and tells them to advance.
        for target in self.targets:
            target.advance()

        # Checks to see if the game has started.
        self.start_game()
        
        # Checks to see if the player has lost yet.
        self.is_game_over = self.game_over()


    def create_target(self):
        """
        Creates a new target of a random type and adds it to the list.
        New targets are created wih 1/50 probability.
        :return:
        """

        # Creates instances of the available target types.
        target = Target()
        strong_target = Strong_target()
        safe_target = Safe_target()

        # Decides which type of target to create.
        target_to_create = random.randint(1, 5)
        #print(target_to_create)
        if target_to_create == 1:
            self.targets.append(target)
        elif target_to_create == 2:
            self.targets.append(strong_target)
        elif target_to_create == 3:
            self.targets.append(safe_target)

    def check_collisions(self):
        """
        Checks to see if bullets have hit targets.
        Updates scores and removes dead items.
        :return:
        """

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
                        self.number_of_targets_shot += 1
                        #self.number_of_points_scored += target.hit()
                    

                        # We will wait to remove the dead objects until after we
                        # finish going through the list
        # Checks for anything that is dead, and removes it
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
        self.number_of_bullets_shot += 1

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
    
    def game_over(self):
        """
        Checks to see if the player is out of time.
        :returns: Boolean
        """
        if self.time <= 0:
            # The game ends. Display game over to the screen.
            return True
        else:
            # Decrements the time
            self.time -= .02
            return False

    def start_game(self):
        """
        Checks to see if the game has started
        """
        if self.time <= 60:
            self.game_started = True
            
    
    def draw_game_over(self):
        """
        Draws GAME OVER to the screen.
        """
        game_over_text = "GAME OVER.".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT / 2
        arcade.draw_text(game_over_text, start_x=start_x, start_y=start_y, font_size=50, color=arcade.color.NAVY_BLUE)
        score_text = "You scored: {} point(s).".format(self.score)
        start_x_2 = 10
        start_y_2 = SCREEN_HEIGHT / 3
        arcade.draw_text(score_text, start_x=start_x_2, start_y=start_y_2, font_size=25, color=arcade.color.NAVY_BLUE)


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, "Awesome Skeet")
arcade.run()
