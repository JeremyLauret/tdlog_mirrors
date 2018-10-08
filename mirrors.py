import lib.Grid as Grid
import lib.LaserBeam as LB
import re

print(" --- DEFINITION DE LA GRILLE --- ")
grid_height = Grid.input_height()
grid_width = Grid.input_width()
Mirrors = Grid.input_mirrors(grid_height, grid_width)

print("Génération de la grille...")
G = Grid.Grid(grid_height, grid_width, Mirrors)
G.display()

print(" --- DEFINITION DU LASER --- ")
Laser = LB.input_laser(grid_height, grid_width)

exit_point, exit_direction, Laser_path = G.compute_laser_beam_path(Laser)
print("Le laser avait pour direction " + exit_direction + " lorsqu'il est sorti en " + exit_point + ".")

display_laser = input("Souhaitez-vous afficher le trajet du laser dans la grille ? [o|N] > ")
if (re.match('ou?i?', display_laser, re.IGNORECASE)):
    G.display(True, Laser_path)