import re
import random

class Grid:
    """
       A Grid class instance is a matrix containing mirrors or two different orientations.

       The Grid class instance is meant to be a gaming board crossed by lasers which are reflected by randomly or
       manually arranged mirrors.
    """

    def __init__(self, height, width, Mirrors):
        """
           :param height: Number of rows of the grid
           :param width: Number of columns of the grid
           :param Mirrors: List of tuples of size 3 containing the coordinates and orientation of each mirror
        """

        self._height = height
        self._width = width
        self._Mirrors = Mirrors


    @property
    def height(self):
        return self._height


    @property
    def width(self):
        return self._width


    @property
    def Mirrors(self):
        return self._Mirrors


    def get_mirror_orientation(self, coord):
        """
            The get_mirror_orientation method returns None if there is no mirror in the cell of coordinates coord.
            If there is a mirror, it returns its orientation ('/' or '\\')
        """
        for k in range(len(self.Mirrors)):
            if (self.Mirrors[k][0:2] == coord):
                return self.Mirrors[k][2]
        return None


    def display(self, display_laser=False, Laser_path=[]):
        """
           The display method prints the Grid instance as a two-dimensionnal matrix containing "/" and "\" symbols
           portraying each mirror and their orientation.
           If the display_laser parameter is set to True, displays the laser path given in parameter.
        """

        firstline = ' '
        for k in range(self.width):
            if (display_laser):
                firstline += ' ' + cap_letter(k) + ' '
            else:
                firstline += cap_letter(k)  # Adds the first capital letters of the alphabet
        print(firstline)

        if (display_laser):
            line_1_char = ' '    # Used to create the second line
            for i in range(self.height):
                line_1 = ' '
                line_2 = cap_letter(i)
                line_3 = ' '
                for j in range(self.width):
                    mirror_orientation = self.get_mirror_orientation((i, j))
                    Visits = get_visits(Laser_path, (i, j))

                    line_1_char = get_first_line_char(Visits)
                    line_1 += ' ' + line_1_char + ' '
                    line_2 += get_second_line(Visits, mirror_orientation, line_1_char)
                    line_3 += ' ' + get_third_line_char(Visits) + ' '

                line_2 += cap_letter(i)
                print(line_1)
                print(line_2)
                print(line_3)

        else :
            for i in range(self.height):
                line = cap_letter(i)
                for j in range(self.width):
                    mirror_orientation = self.get_mirror_orientation((i, j))
                    if (mirror_orientation != None):    # If there is a mirror in this cell
                        line += mirror_orientation
                    else:
                        line += ' '
                line += cap_letter(i)
                print(line)

        print(firstline)    # The first and last lines are identical


    def compute_laser_beam_path(self, laser_beam):
        """
           Returns a list Laser_path containing the cell-to-cell progress of the LaserBeam instance given.

           Each element of Laser_path is a size 3 tuple.
           Each tuple contains the coordinates of a visited cell, the orientation of the LaserBeam object
           when it entered this cell, and its orientation when it left it.

           :type arg1: LaserBeam
        """

        Laser_path = []    # List of the coordinates and in and out directions of the laser beam in each cell it visits

        # Progress of the laser beam
        while (0 <= laser_beam.coordinates[0] < self.height and 0 <= laser_beam.coordinates[1] < self.width):
            # If there is a mirror in this cell
            mirror_orientation = self.get_mirror_orientation(laser_beam.coordinates)
            former_direction = laser_beam.direction

            if (mirror_orientation != None):
                laser_beam.bounce(mirror_orientation)  # The direction of the laser beam changes

            Laser_path.append((laser_beam.coordinates, former_direction, laser_beam.direction))
            laser_beam.progress()

        # Computing of the exit point
        exit_point = cap_letter(laser_beam.coordinates[0]) \
                     if laser_beam.coordinates[1] < 0 or laser_beam.coordinates[1] >= self.width \
                     else cap_letter(laser_beam.coordinates[1])

        return exit_point, laser_beam.direction, Laser_path


def get_visits(Laser_path, coord):
    """
       Returns a list of all the elements of Laser_path deprived of their first element whose coordinates are
       equal to coord.
       To know what Laser_path contains, see the compute_laser_beam_path method documentation.
    """

    Visits = []
    for k in range(len(Laser_path)):
        if (Laser_path[k][0] == coord):
            Visits.append(Laser_path[k][1:3])
    return Visits


def get_first_line_char(Visits):
    """
       This function is used to set the content of the first line of a given cell in the Grid.display method.
    """
    for k in range(len(Visits) - 1, -1, -1):    # Decreasing order
        if (Visits[k][0] == 'v'):    # The beam enters through the top
            return 'v'
        if (Visits[k][1] == '^'):    # The beam exits through the top
            return '^'
    return ' '    # If the beam never goes through the top


def get_second_line(Visits, mirror_orientation, first_line_char):
    """
       This function is used to set the content of the second line of a given cell in the Grid.display method.
    """

    k = len(Visits) - 1
    cont_left = True     # Becomes False if a first character has been found
    cont_right = True    # Becomes False if a third character has been found
    first_char = ' '
    third_char = ' '
    while((cont_left or cont_right) and k > -1):    # Decreasing order
        if (cont_left):
            if (Visits[k][0] == '>'):    # The beam enters through the left
                first_char = '>'
                cont_left = False
            if (Visits[k][1] == '<'):    # The beam exits through the left
                first_char = '<'
                cont_left = False
        if (cont_right):
            if (Visits[k][0] == '<'):    # The beam enters through the right
                third_char = '<'
                cont_right = False
            if (Visits[k][1] == '>'):    # The beam exits through the right
                third_char = '>'
                cont_right = False
        k -= 1
    if (mirror_orientation != None):    # The cell contains a mirror
        second_char = mirror_orientation
    else:
        second_char = first_char if first_char != ' ' else first_line_char

    return first_char + second_char + third_char


def get_third_line_char(Visits):
    """
       This function is used to set the content of the third line of a given cell in the Grid.display method.
    """
    for k in range(len(Visits) - 1, -1, -1):    # Decreasing order
        if (Visits[k][0] == '^'):    # The beam enters through the bottom
            return '^'
        if (Visits[k][1] == 'v'):    # The beam exits through the bottom
            return 'v'
    return ' '    # If the beam never goes through the bottom


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


def is_valid_length(value, min, max):
    """
       The is_valid_length function indicates if the given parameter value is an integer comprised between the
       min and max parameters.

       If one of the conditions is not met, the function prints an appropriate message and returns False.
       Else, it returns True.

       :Example:

       >>> is_valid_length('1.1', 0, 10)
       Erreur : la valeur fournie n'est pas un entier.
       False
       >>> is_valid_length('-1', 0, 10)
       Erreur : la valeur fournie doit être supérieure à 0.
       False
       >>> is_valid_length('2', 0, 10)
       True
    """

    try:
        value = int(value)
    except:
        print("Erreur : la valeur fournie n'est pas un entier.")
        return False

    if (value < min):
        print("Erreur : la valeur fournie doit être supérieure à " + str(min) + ".")
        return False

    if(value > max):
        print("Erreur : la valeur fournie doit être inférieure à " + str(max) + ".")
        return False

    return True


def is_valid_probability(probability):
    """
       returns True if probability is castable as a float and ranges between 0 and 1
    """
    try:
        probability_float = float(probability)
    except:
        print("Erreur : la valeur fournie n'est pas un nombre !")
        return False

    if (probability_float < 0 or probability_float > 1):
        print("Erreur : la valeur fournie doit être entre 0 et 1.")
        return False

    return True


def is_valid_mirror(mirror, height, width):
    r"""
       The is_valid_mirror function indicates if the given parameter mirror has valid coordinates and orientation
       character.

       If one of the conditions is not met, the function prints an appropriate message and returns False.
       Else, it returns True.

       :Example:

       >>> is_valid_mirror((1.2, 1, '/'), 10, 10)
       Erreur : les coordonnées fournies sont invalides.
       False
       >>> is_valid_mirror((12, 1, '/'), 10, 10)
       Erreur : les coordonnées fournies sont invalides.
       False
       >>> is_valid_mirror((2, 3, 'Hello'), 10, 10)
       Erreur : l'orientation du miroir n'a pu être reconnue.
       False
       >>> is_valid_mirror((2, 3, '\\'), 10, 10)
       True
    """

    try:
        i = int(mirror[0])
        j = int(mirror[1])
    except:
        print("Erreur : les coordonnées fournies sont invalides.")
        return False

    if (i < 0 or i >= height or j < 0 or j >= width):
        print("Erreur : les coordonnées fournies sont invalides.")
        return False

    if(not mirror[2] in ['/', '\\']):
        print("Erreur : l'orientation du miroir n'a pu être reconnue.")
        return False

    return True


def input_width():
    grid_width_str = input("Quelle largeur de grille désirez-vous ? > ")
    while (not is_valid_length(grid_width_str, 3, 26)):
        grid_width_str = input("Quelle largeur de grille désirez-vous ? > ")
    return int(grid_width_str)


def input_height():
    grid_height_str = input("Quelle hauteur de grille désirez-vous ? > ")
    while (not is_valid_length(grid_height_str, 3, 26)):
        grid_height_str = input("Quelle hauteur de grille désirez-vous ? > ")
    return int(grid_height_str)


def input_mirrors(grid_height, grid_width):
    Mirrors = []
    manual_mirrors = input("Souhaitez-vous définir les miroirs manuellement ? [O|n] > ")

    if (re.match('no?n?', manual_mirrors, re.IGNORECASE)): # Miroirs définis aléatoirement
        print("Les miroirs vont être disposés aléatoirement dans la grille. "
              "Les deux orientations / et \\ sont équiprobables.")

        probability = input("Quelle doit être la probabilité pour une case d'être occupée par un miroir ? [0..1] > ")
        while(not is_valid_probability(probability)):
            probability = input("Quelle doit être la probabilité pour une case d'être occupée par un miroir ? [0..1] > ")

        for i in range(grid_height):
            for j in range(grid_width):
                place_mirror = random.uniform(0, 1)
                if (place_mirror < float(probability)):
                    orientation = random.choice(['/', '\\'])
                    Mirrors.append((i, j, orientation))
        return Mirrors

    print("Veuillez entrer pour chaque miroir ses ligne, colonne et orientation. "
          "Entrez \"Stop\" pour mettre fin à la séquence d'ajout de miroirs.")
    cont = True
    count = 1
    while(cont):
        print("Mirroir n°", count, sep="")
        row = input("Ligne [A|B|...] : > ")
        if (re.match('stop', row, re.IGNORECASE)):
            break
        col = input("Colonne [A|B|...] : > ")
        if (re.match('stop', col, re.IGNORECASE)):
            break
        orientation = input("Orientation [/|\\] : > ")
        if (re.match('stop', orientation, re.IGNORECASE)):
            break

        try:
            mirror = (letter_rank(row), letter_rank(col), orientation)
        except:
            print("Erreur : le miroir fourni est invalide.")
            print(" ")
            continue

        if(is_valid_mirror(mirror, grid_height, grid_width)):
            Mirrors.append(mirror)
            count += 1

    return Mirrors