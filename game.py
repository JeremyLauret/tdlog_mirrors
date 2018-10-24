import lib.grid as grid
import lib.laser as laser
import lib.mirrors as mirrors
import lib.teleporter as teleporter
import lib.string_utils as string_utils
import conf
import re

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
        if type == 'o':
            items.append((row, col, teleporter.Teleporter(row, col)))
        elif type == '\\' :
            items.append((row, col, mirrors.BackslashMirror()))
        elif type == '/' :
            items.append((row, col, mirrors.SlashMirror()))
        elif type == '#' :
            items.append((row, col, mirrors.HashMirror()))
        elif type == '|' :
            items.append((row, col, mirrors.PipeMirror()))
        elif type == '-' :
            items.append((row, col, mirrors.DashMirror()))
        else:
            print("Erreur : type d'objet inconnu.")
            continue
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

def build_conclusion(grid, exit_x, exit_y, exit_direction):
    """
       Builds the conclusion text summing up the exit point and direction of
       the laser after a simulation.
    """
    if exit_x < 0 or exit_x >= grid.height:
        exit_point = string_utils.rank_to_cap_letter(exit_y)
        return ("Le laser quitte la grille au point {} avec pour direction {}."
                .format(exit_point, exit_direction))
    elif exit_y < 0 or exit_y >= grid.width:
        exit_point = string_utils.rank_to_cap_letter(exit_x)
        return ("Le laser quitte la grille au point {} avec pour direction {}."
                .format(exit_point, exit_direction))
    # Le laser a disparu dans un téléporteur
    exit_point = (string_utils.rank_to_cap_letter(exit_x),
                  string_utils.rank_to_cap_letter(exit_y))
    return ("Le laser est aspiré par un téléporteur sans sortie ! Il disparait"
            " au point ({}, {}) avec direction {}."
            .format(exit_point[0], exit_point[1], exit_direction))
              
def build_conclusions(grid, exit_data):
    """
       Builds the conclusion text summing up the exit points and directions the
       laser could have depending on the teleporters it encounters.
       
       :param exit_data: 
       List of size 3 tuples in the form (exit_x, exit_y, exit_direction).
    """
    if (len(exit_data) == 1):    # Si un seul résultat est possible
        return (build_conclusion(grid, exit_data[0][0], exit_data[0][1],
                exit_data[0][2]))
    text = "Les résultats possibles de la simulation sont les suivants :\n"
    counter = 1
    for data in exit_data:
        text += (str(counter) + ") "
                 + build_conclusion(grid, data[0], data[1], data[2]) + "\n")
        counter += 1
    return text
    
def display_conclusion(grid, exit_data):
    print(build_conclusions(grid, exit_data))

def play():
    Grid = input_grid()
    print(Grid)
    Laser = input_laser(Grid)
    compute_all_paths = input("Calculer chaque sortie possible ? [O|n] > ")
    print(" ")
    if (re.match('no?n?', compute_all_paths, re.IGNORECASE)):
        exit_data = Grid.compute_laser_exit(Laser)
        display_laser_path = input("Afficher le trajet du laser ? [O|n] > ")
        if (not re.match('no?n?', display_laser_path, re.IGNORECASE)):
            Grid.display_laser(Laser)
    else:
        exit_data = Grid.compute_all_laser_exits(Laser)
    display_conclusion(Grid, exit_data)

if __name__ == '__main__':
    play()