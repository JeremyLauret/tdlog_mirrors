class LaserBeam:
    DIRECTIONS = {'>': (0, 1), 'v': (1, 0), '<': (0, -1), '^': (-1, 0)}
    BOUNCE_SLASH = {'>': '^', 'v': '<', '<': 'v', '^': '>'}
    BOUNCE_BACKSLASH = {'>': 'v', 'v': '>', '<': '^', '^': '<'}

    def __init__(self, entry_point, entry_direction, grid_heigth, grid_width):
        self._direction = entry_direction
        if (entry_direction in ['<', '>']):
            self.coordinates = (letter_rank(entry_point), 0 if entry_direction == '>' else grid_width - 1)
        else:
            self.coordinates = (0 if entry_direction == 'v' else grid_heigth - 1, letter_rank(entry_point))

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        assert (value in ['>', '<', '^', 'v'])
        self._direction = value

    def bounce(self, mirror_nature):
        """
           Changes the laser's direction by bouncing on the given mirror
        """

        assert(mirror_nature in ['/', '\\'])
        self.direction = LaserBeam.BOUNCE_SLASH[self.direction] if mirror_nature == '/' \
                         else LaserBeam.BOUNCE_BACKSLASH[self.direction]

    def progress(self):
        """
           Upon call, the laser beam progresses one cell further.
        """
        self.coordinates = tuple(map(sum, zip(self.coordinates, LaserBeam.DIRECTIONS[self.direction])))



def letter_rank(cap_letter):
    """
       Returns the rank in the alphabet of the given capital letter

       :Example:

       >>> letter_rank('A')
       0
       >>> letter_rank('C')
       2
    """

    return ord(cap_letter) - ord('A')


def cap_letter(numb):
    """
       Returns the capital letter of rank numb in the alphabet

       :Example:

       >>> cap_letter(0)
       'A'
       >>> cap_letter(2)
       'C
    """

    return chr(ord('A') + numb)


def is_valid_laser(entry_point, direction, grid_height, grid_width):
    """
        The is_valid_laser function indicates if the entry_point and direction given are compatible with the specified
        grid size.

        If one of the conditions is not met, the function prints an appropriate message and returns False.
        Else, it returns True.

        :Example:

        >>> is_valid_laser('C', 'Hello', 10, 10)
        Erreur : la direction fournie est invalide.
        False
        >>> is_valid_laser('Z', '>', 10, 10)
        "Erreur : le point d'entrée est incompatible avec la direction fournie."
        False
        >>> is_valid_laser('C', '>', 10, 10)
        True
    """

    if (not direction in ['<', '^', '>', 'v']):
        print("Erreur : la direction fournie est invalide.")
        return False

    try:
        entry_point_int = letter_rank(entry_point)
    except:
        print("Erreur : le point d'entrée fourni est un caractère invalide.")
        return False

    if (direction in ['<', '>']):  # The laser beam enters from left or right
        if (entry_point_int < 0 or entry_point_int >= grid_height):
            print("Erreur : le point d'entrée est incompatible avec la direction fournie.")
            return False

        return True

    # The laser beam enters from top or bottom
    if (entry_point_int < 0 or entry_point_int >= grid_width):
        print("Erreur : le point d'entrée est incompatible avec la direction fournie.")
        return False

    return True


def input_laser(grid_height, grid_width):
    entry_point = input("Quel doit être le point d'entrée du rayon laser ? > ")
    direction = input("Quelle doit être la direction du laser ? [>|<|^|v] > ")

    while(not is_valid_laser(entry_point, direction, grid_height, grid_width)):
        entry_point = input("Quel doit être le point d'entrée du rayon laser ? > ")
        direction = input("Quelle doit être la direction du laser ? [>|<|^|v] > ")

    return LaserBeam(entry_point, direction, grid_height, grid_width)