import conf
import lib.mirrors as mirrors
import lib.teleporter as teleporter
import lib.string_utils as string_utils
import lib.laser

class Grid:
    """
       A Grid is a matrix containing mirrors and teleporters.
       It is meant to be crossed by a laser which interacts with the contents of
       the grid.
    """
    def __init__(self, height, width, items):
        assert conf.min_height <= height <= conf.max_height, \
            "Error : height of size {} is not allowed.".format(height)
        assert conf.min_width <= width <= conf.max_width, \
            "Error : width of size {} is not allowed.".format(width)
        self._items = dict()    
        self._height = height
        self._width = width
        # List of size 2 tuples (x, y) depicting the coordinates of the
        # teleporters contained in the grid
        self._teleporters_coordinates = []
        # List of size 3 tuples (x, y, dir), each depicting a teleporter from 
        # which at least one laser exited with direction dir
        self._teleporters_exited = []
        for (x, y, item) in items:
            assert (0 <= x < height) and (0 <= y < width), \
                "Error : coordinates ({},{}) are invalid.".format(x, y)
            assert item.symbol in conf.allowed_items, ("Error : {} is not a "
                   "valid item.".format(item.symbol))
            self._items[x, y] = item
            if item.symbol == 'o':
                self.add_teleporter_coordinates(x, y)

    @property
    def height(self):
        return self._height
    @property
    def width(self):
        return self._width
    @property
    def teleporters_coordinates(self):
        return self._teleporters_coordinates
    @property
    def teleporters_exited(self):
        return self._teleporters_exited

    def add_teleporter_coordinates(self, x, y):
        """
           Appends the given coordinates to _teleporters_coordinates.
        """
        self._teleporters_coordinates.append((x, y))
        
    def add_teleporter_exited(self, x, y, direction):
        """
           Appends the given teleporter coordinates and direction to
           _teleporters_exited.
        """
        self._teleporters_exited.append((x, y, direction))

    def __getitem__(self, key):
        """
           :return: The item contained in the slot of coordinates key.
        """
        x, y = key
        assert (0 <= x < self.height) and (0 <= y < self.width), ("Error : "
                "coordinates ({},{}) are invalid.".format(x, y))
        if key in self._items:
            return self._items[key]
        else:
            return mirrors.EmptyMirror()

    def build_displayal(self, laser=None):
        """
           Builds the strings used in the __str__ and display_laser methods.
           If no laser is given, the symbols of the contents of the grid will be
           added to the string.
           If a laser is given, its path will be added to the string as dots.
        """
        text = ""
        firstline = " "
        for k in range(self.width):
            firstline += string_utils.rank_to_cap_letter(k)
        firstline += "\n"
        text += firstline
        for i in range(self.height):
            line = string_utils.rank_to_cap_letter(i)
            if laser == None:
                for j in range(self.width):
                    line += self[i, j].symbol
            else :
                for j in range(self.width):
                    if (laser.path[i][j]):
                        line += "."
                    else:
                        line += " "
            line += string_utils.rank_to_cap_letter(i) + "\n"
            text += line
        text += firstline    # The first and last lines are identical
        return text

    def __str__(self):
        """
           Displays the grid and its contents
        """
        return self.build_displayal()

    def display_laser(self, laser):
        """
           Displays the grid and the path of laser
        """
        print(self.build_displayal(laser))


    def compute_laser_exit(self, laser):
        """
           Makes the given laser progress in the grid with the random effect of
           the teleporters up to its stop or exit.
           Returns the exit point and exit direction of the laser (a laser which
           stopped due to a lone teleporter exits the grid in this cell).
        """
        while (0 <= laser.x < self.height and 0 <= laser.y < self.width
               and not laser.stop):
            self[laser.x, laser.y].interact_with_laser(laser)
            if (not laser.stop):
                laser.progress()
        return [(laser.x, laser.y, laser.direction)]
        
    def compute_all_laser_exits(self, laser):
        """
           Makes the given laser progress in the grid up to its stop or exit.
           An encounter with a teleporter will cause copies of the laser to run
           through all possible paths except one and recursively return the exit
           points and directions of each of these paths, while the laser itself
           will go through the first possible path.
           
           :return: The list of the exit points and directions the laser could
                    have depending on the teleporters it encounters.
        """
        exit_data = []
        while (0 <= laser.x < self.height and 0 <= laser.y < self.width
               and not laser.stop):
            interesting_coordinates = (self[laser.x, laser.y]
                                      .interact_with_laser(laser, random=False))
            if (interesting_coordinates != None):    # Teleporter encounter
                if (len(interesting_coordinates) == 0):
                    return exit_data    # The laser cannot give new exit points
                for coordinates in interesting_coordinates[1:]:
                    laser_copy = lib.laser.Laser(laser.x, laser.y,
                                                 laser.direction, self)
                    laser_copy.teleport(coordinates)
                    laser_copy.progress()
                    exit_data += self.compute_all_laser_exits(laser_copy)
                laser.teleport(interesting_coordinates[0])
            if (not laser.stop):
                laser.progress()
        exit_data.append((laser.x, laser.y, laser.direction))
        return exit_data