class Mirror():
    """
       Abstract class for mirrors contained in the grid.
    """
    def __init__(self):
        pass

    def interact_with_laser(self, laser, random=True):
        """
           Reflects the given laser on the mirror and returns None for the laser
           not to duplicate.
        """
        laser.direction = self._DIRECTIONS[laser.direction]

class BackslashMirror(Mirror):
    """
       A backslash mirror '\' reflects lasers from every direction in a 90°
       angle.
    """
    _DIRECTIONS = {'>': 'v', 'v': '>', '<': '^', '^': '<'}
    @property
    def symbol(self):
        return '\\'

class DashMirror(Mirror):
    """
       A dash mirror '-' reflects lasers from top and bottom in a 180° angle.
    """
    _DIRECTIONS = {'>': '>', '<': '<', 'v': '^', '^': 'v'}
    @property
    def symbol(self):
        return '-'

class EmptyMirror(Mirror):
    """
       An empty mirror ' ' doesn't alter lasers
    """
    _DIRECTIONS = {'>': '>', '<': '<', '^': '^', 'v': 'v'}
    @property
    def symbol(self):
        return ' '

class HashMirror(Mirror):
    """
       A hash mirror '#' reflects lasers from any direction in a 180° angle.
    """
    _DIRECTIONS = {'>': '<', '<': '>', 'v': '^', '^': 'v'}
    @property
    def symbol(self):
        return '#'

class PipeMirror(Mirror):
    """
       A pipe mirror '|' reflects lasers from left and right in a 180° angle.
    """
    _DIRECTIONS = {'>':'<', '<':'>', 'v':'v', '^':'^'}
    @property
    def symbol(self):
        return '|'

class SlashMirror(Mirror):
    """
       A slash mirror '/' reflects lasers from every direction in a 90° angle.
    """
    _DIRECTIONS = {'>':'^', '^':'>', '<':'v', 'v':'<'}
    @property
    def symbol(self):
        return '/'