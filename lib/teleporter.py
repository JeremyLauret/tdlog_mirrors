import random as rd

class Teleporter():
    """
       A teleporter 'o' teleports lasers to another teleporter picked at random.
    """
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def symbol(self):
        return 'o'

    def teleport(self, laser, teleporters_coordinates):
        """
           Teleports the given laser to another teleporter of coordinates picked
           at random in teleporters.coordinates.
        """
        if (len(teleporters_coordinates) == 1):    # There is only one teleporter in the grid
            laser.vanish()
        else:
            random_coordinates = rd.choice([xy for xy in teleporters_coordinates if xy != (self._x, self._y)])
            laser.teleport(random_coordinates)