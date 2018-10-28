from random import randint, choice
import conf
import back.mirrors as mirrors
import back.teleporter as teleporter
import back.grid as grid
import back.laser as laser
import back.string_utils as string_utils

def build_item(row, col, type):
    """
    :return: A mirror with the given type, or a teleporter with the given
             coordinates.
    """
    if type == 'o':
        return teleporter.Teleporter(row, col)
    elif type == '\\':
        return mirrors.BackslashMirror()
    elif type == '/':
        return mirrors.SlashMirror()
    elif type == '#':
        return mirrors.HashMirror()
    elif type == '|':
        return mirrors.PipeMirror()
    elif type == '-':
        return mirrors.DashMirror()
    print("Erreur : type d'objet inconnu.")
    return None

def input_grid():
    """
       Builds a Grid object from user input.
    """
    valid_dimensions = False
    while (not valid_dimensions):
        try:
            height = int(input("Hauteur de la grille ? [{}..{}] > ".format(
                     conf.min_height, conf.max_height)))
            width = int(input("Largeur de la grille ? [{}..{}] > ".format(
                    conf.min_width, conf.max_width)))
        except:
            print("Erreur : les dimensions fournies doivent être des entiers.")
            continue
        if not (conf.min_width <= width <= conf.max_width and conf.min_height
                <= height <= conf.max_height):
            print("Erreur : les dimensions fournies sont invalides")
            continue
        valid_dimensions = True
    print("Début de la séquence d'ajout de miroirs et téléporteurs...entrez"
          " \"Stop\" pour y mettre fin.")
    items = []
    count = 1
    while (True):
        print(" ")
        print(" -- Miroir/Téléporteur n°{} -- ".format(count))
        print(" Entrez \"Stop\" pour quitter.")
        row_str = input("Ligne ? [A|B|...] : > ")
        if (string_utils.case_insensitive_stop(row_str)):
            break
        col_str = input("Colonne ? [A|B|...] : > ")
        if (string_utils.case_insensitive_stop(col_str)):
            break
        try:
            row = string_utils.cap_letter_to_rank(row_str)
            col = string_utils.cap_letter_to_rank(col_str)
            assert 0 <= row < height and 0 <= col < width
        except:
            print("Erreur : les coordonnées fournies sont invalides.")
            continue
        type = input("Type ? [/|\\|#|||-|o] : > ")
        if (string_utils.case_insensitive_stop(type)):
            break
        item = build_item(row, col, type)
        if (item == None):    # Type not recognized
            continue
        items.append((row, col, item))
        count += 1
    return grid.Grid(height, width, items)

def input_laser(container):
    """
       Builds a Laser object entering in container from user input.
    """
    valid_input = False
    while(not valid_input):
        try:
            direction = input("Direction initiale du laser ? [>|<|^|v] > ")
            assert direction in conf.allowed_directions
        except:
            "Erreur : direction invalide."
            continue
        try:
            entry_point = string_utils.cap_letter_to_rank(input("Point"
                          " d'entrée du laser ? [A|B|...] > "))
            if direction in ['>', '<']:
                assert 0 <= entry_point < container.height
            else:
                assert 0 <= entry_point < container.width
        except:
            "Erreur : point d'entrée invalide pour la direction fournie."
            continue
        valid_input = True
    if direction in ['>', '<']:
        x, y = entry_point, 0 if direction == '>' else container.width - 1
    else:
        x, y = 0 if direction == 'v' else container.height - 1, entry_point
    return laser.Laser(x, y, direction, container)

def random_grid(min_height, max_height, min_width, max_width,
                min_items, max_items):
    """
       Builds a grid object with random size and content.
       The mirror/teleporter type choice is biased so that it is three times as
       likely to chose a teleporter as any mirror.
       A teleporter is added if there is only one teleporter in the grid to
       prevent the laser from vanishing.
    """
    assert conf.min_height <= min_height and max_height <= conf.max_height, \
        "Error : the height range [{}, {}] is not contained in [{}, {}]." \
        .format(min_height, max_height, conf.min_height, conf.max_height)
    assert conf.min_width <= min_width and max_width <= conf.max_width, \
        "Error : the width range [{}, {}] is not contained in [{}, {}]." \
        .format(min_width, max_width, conf.min_width, conf.max_width)
    grid_height = randint(min_height, max_height)
    grid_width = randint(min_width, max_width)
    items_number = randint(min_items, max_items)
    empty_coordinates = sum([[(i, j) for j in range(grid_width)]
                       for i in range(grid_height)], [])
    items = []
    for item_number in range(items_number):
        random_cell_number = randint(0, len(empty_coordinates) - 1)
        random_row, random_col = empty_coordinates[random_cell_number]
        empty_coordinates = (empty_coordinates[:random_cell_number]
                       + empty_coordinates[random_cell_number + 1:])
        random_type = choice(conf.allowed_items + ['o', 'o'])
        items.append((random_row, random_col,
                      build_item(random_row, random_col, random_type)))
    if [item[2].symbol for item in items].count('o') == 1:
        random_row, random_col = choice(empty_coordinates)
        items.append((random_row, random_col,
                      build_item(random_row, random_col, 'o')))
    return grid.Grid(grid_height, grid_width, items)

def random_laser(_grid):
    """
       Builds a laser object entering the grid _grid from a random cell on the
       side.
    """
    random_direction = choice(conf.allowed_directions)
    if random_direction in ['>', '<']:
        random_x, random_y = (randint(0, _grid.height - 1), 0 if
                              random_direction == '>' else _grid.width - 1)
    else:
        random_x, random_y = (0 if random_direction == 'v' else
                              _grid.height - 1, randint(0, _grid.width - 1))
    return laser.Laser(random_x, random_y, random_direction, _grid)