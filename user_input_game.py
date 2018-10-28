import re
import back.string_utils as string_utils
import front.creation_tools as creation_tools

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
    _grid = creation_tools.input_grid()
    print(_grid)
    _laser = creation_tools.input_laser(_grid)
    compute_all_paths = input("Calculer chaque sortie possible ? [O|n] > ")
    print(" ")
    if (re.match('no?n?', compute_all_paths, re.IGNORECASE)):
        exit_data = _grid.compute_laser_exit(_laser)
        display_laser_path = input("Afficher le trajet du laser ? [O|n] > ")
        if (not re.match('no?n?', display_laser_path, re.IGNORECASE)):
            _grid.display_laser(_laser)
    else:
        exit_data = _grid.compute_all_laser_exits(_laser)
    display_conclusion(_grid, exit_data)

if __name__ == '__main__':
    play()