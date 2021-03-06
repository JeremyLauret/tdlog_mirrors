import conf

class Laser:
    """
       A laser enters a grid from one side and usually escapes from another
       after interacting with the items contained in the grid.
       A lone teleporter may stop the laser.
    """
    def __init__(self, initial_x, initial_y, initial_direction, container):
        assert (0 <= initial_x <= container.height - 1) and (0 <= initial_y
                <= container.width - 1), "Error : invalid laser entry point."
        assert initial_direction in conf.allowed_directions, ("Error : invalid "
               "laser initial direction.")
        self._container = container
        self._x = initial_x
        self._y = initial_y
        self._direction = initial_direction
        # _path depicts the visited cells of the grid
        self._path = [[False for j in range(container.width)]
                      for i in range(container.height)]
        self._stop = False    # Shows if the laser encounters a lone teleporter

    @property
    def x(self):
        return self._x
    @property
    def y(self):
        return self._y
    @property
    def direction(self):
        return self._direction
    @property
    def path(self):
        return self._path
    @property
    def stop(self):
        return self._stop
    @property
    def container(self):
        return self._container

    @direction.setter
    def direction(self, input_direction):
        assert input_direction in conf.allowed_directions, ("Error : invalid "
               "laser direction.")
        self._direction = input_direction
    @stop.setter
    def stop(self, input_stop):
        assert input_stop == True or input_stop == False, ("Error : invalid "
               "stop value.")
        self._stop = input_stop

    def progress(self):
        """
           Upon call, the laser progresses one cell further.
        """
        self._path[self.x][self.y] = True
        if self.direction == '>':
            self._y += 1
        elif self.direction == '<':
            self._y -= 1
        elif self.direction == 'v':
            self._x += 1
        else:
            self._x -= 1

    def teleport(self, coordinates):
        """
           Teleports the laser to the given coordinates.
        """
        self._path[self.x][self.y] = True
        assert 0 <= coordinates[0] <= self._container.height, ("Error : invalid"
               " teleportation coordinates.")
        assert 0 <= coordinates[1] <= self._container.width, ("Error : invalid "
               "teleportation coordinates.")
        self._x, self._y = coordinates
        self._container.add_teleporter_exited(self._x, self._y, self._direction)

    def vanish(self):
        """
           Stops the laser
        """
        self._path[self.x][self.y] = True
        self.stop = True
