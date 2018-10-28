from random import choice

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

    def interact_with_laser(self, laser, random=True):
        """
           Makes the laser vanish if only one teleporter exists.
           If random is true, teleports the given laser to another teleporter of
           coordinates picked at random in _teleporters_coordinates.
           If random is false, returns the list of all interesting teleporters
           to teleport to, in the sense that they haven't been exited with
           laser.direction yet.
        """
        teleporters_coordinates = laser.container.teleporters_coordinates
        other_teleporters = [xy for xy in teleporters_coordinates
                             if xy != (self._x, self._y)]
        if (len(other_teleporters) == 0):    # Only one teleporter in the grid
            laser.vanish()
        elif random:
            random_coordinates = choice(other_teleporters)
            laser.teleport(random_coordinates)
        else:
            return [xy for xy in other_teleporters if (xy[0], xy[1],
                    laser.direction) not in laser.container.teleporters_exited]