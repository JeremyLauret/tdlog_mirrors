import conf
import lib.mirrors as mirrors
import lib.teleporter as teleporter
import lib.string_utils as string_utils

class Grid:
    """
       A Grid is a matrix containing mirrors and teleporters.
       It is meant to be crossed by a laser which interacts with the contents of the grid.
    """
    def __init__(self, height, width, items):
        assert conf.min_height <= height <= conf.max_height, \
            "Error : height of size {} is not allowed.".format(height)
        assert conf.min_width <= width <= conf.max_width, \
            "Error : width of size {} is not allowed.".format(width)
        self._items = dict()
        self._teleporters_coordinates = []     # Coordinates of the teleporters contained in the grid
        self._height = height
        self._width = width
        for (x, y, item) in items:
            assert (0 <= x < height) and (0 <= y < width), \
                "Error : coordinates ({},{}) are invalid.".format(x, y)
            assert item.symbol in conf.allowed_items, "Error : {} is not a valid item.".format(item.symbol)
            self._items[x, y] = item
            if (item.symbol == 'o'):
                self._teleporters_coordinates.append((x, y))

    @property
    def height(self):
        return self._height
    @property
    def width(self):
        return self._width
    @property
    def teleporters_coordinates(self):
        return self._teleporters_coordinates

    def __getitem__(self, key):
        """
        :return: The item contained
        """
        x, y = key
        assert (0 <= x < self.height) and (0 <= y < self.width), \
            "Error : coordinates ({},{}) are invalid.".format(x, y)
        if key in self._items:
            return self._items[key]
        else:
            return mirrors.EmptyMirror()

    def build_displayal(self, laser=None):
        """
           Builds the strings displayed in the __str__ and display_laser methods.
           If no laser is given, the symbols of the contents of the grid will be added to the string.
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
           Makes the given laser progress in the grid up to its stop or exit.
           Returns the exit point and exit direction of the laser (a laser which stopped due to a
           lone teleporter is expected to exit the grid in this cell).
        """
        while (0 <= laser.x < self.height and 0 <= laser.y < self.width and not laser.stop):
            if (isinstance(self[laser.x, laser.y], teleporter.Teleporter)):
                self[laser.x, laser.y].teleport(laser, self.teleporters_coordinates)
            else:
                self[laser.x, laser.y].reflect(laser)
            if (not laser.stop):
                laser.progress()
        return laser.x, laser.y, laser.direction