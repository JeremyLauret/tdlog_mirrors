import random as rd

class Teleporter():
    """
       A teleporter 'o' teleports lasers to another teleporter picked at random.
    """
    _teleporters_coordinates = []
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self.add_teleporter_coordinates(x, y)

    @property
    def symbol(self):
        return 'o'
        
    @classmethod
    def add_teleporter_coordinates(cls, x, y):
        """
           Appends the given teleporter coordinates to _teleporters_coordinates
        """
        cls._teleporters_coordinates.append((x, y))
        
    @classmethod
    def wipe_teleporter_coordinates(cls):
        """
           Empties _teleporters_coordinates
        """
        cls._teleporters_coordinates = []

    def interact_with_laser(self, laser, random=True):
        """
           Makes the laser vanish if only one teleporter exists.
           If random is true, teleports the given laser to another teleporter of
           coordinates picked at random in _teleporters_coordinates.
           If random is false, returns the list of all interesting teleporters
           to teleport to, in the sense that they haven't been exited with
           laser.direction yet.
        """
        other_teleporters = [xy for xy in self._teleporters_coordinates 
                             if xy != (self._x, self._y)]
        if (len(other_teleporters) == 0):    # Only one teleporter in the grid
            laser.vanish()
        elif random:
            random_coordinates = rd.choice(other_teleporters)
            laser.teleport(random_coordinates)
        else:
            return [xy for xy in other_teleporters if (xy[0], xy[1],
                    laser.direction) not in laser.container.teleporters_exited]