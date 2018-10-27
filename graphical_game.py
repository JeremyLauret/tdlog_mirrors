import sys
from PyQt4 import QtGui, QtCore
from random import randint, choice
import conf
import lib.grid as grid
import lib.laser as laser
import game

MIN_HEIGHT = 4
MAX_HEIGHT = 6
MIN_WIDTH = 4
MAX_WIDTH = 6
MIN_ITEMS_NUMBER = 4
MAX_ITEMS_NUMBER = 6
IMAGE_FOLDER = 'img/'

class ExitButton(QtGui.QPushButton):
    """
       A button with a set of coordinates.
    """
    def __init__(self, text, row, col):
        super().__init__(text)
        self._row = row
        self._col = col
    @property
    def row(self):
        return self._row
    @property
    def col(self):
        return self._col

class VerticalExitButton(ExitButton):
    """
       An exit button on the left or right sides of the grid.
       Its width is fixed to the default height of a QPushButton in the given
       widget.
    """
    def __init__(self, text, row, col):
        super().__init__(text, row, col)
        # Enable height resizing and fix width to the default button height
        self.setSizePolicy(QtGui.QSizePolicy.Fixed,
                           QtGui.QSizePolicy.Expanding)
        self.setFixedWidth(QtGui.QPushButton().sizeHint().height())

class CenteredBoldLabel(QtGui.QLabel):
    """
       A label with a centered bold text.
    """
    def __init__(self, text):
        super().__init__(text)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setFont(QtGui.QFont("Sans Serif", weight=QtGui.QFont.Bold))

class ItemLabel(QtGui.QLabel):
    """
       A label depicting a mirror or a teleporter.
       Its square shape remains unchanged after resizing.
    """
    def __init__(self, image_path):
        super().__init__()
        self.setPixmap(QtGui.QPixmap(image_path))
        self.setScaledContents(True)

    def resizeEvent(self, event):
        if event.size().width() > event.size().height():
            self.resize(event.size().height(), event.size().height())
        else:
            self.resize(event.size().width(), event.size().width())

class GameGui(QtGui.QWidget):
    """
       The main graphic user interface, consisting of a grid filled with
       mirrors and teleporters, as well as buttons on the sides for the player
       to guess a laser exit.
    """
    def __init__(self, _grid, _laser):
        super().__init__()
        self._grid = _grid
        self._laser = _laser
        self.keep_playing = False    # The player does not want to try again
        self._buttons_active = False    # The buttons are not yet active
        self._side_labels = []    # List of question mark labels
        print(self._grid)
        self._graphic_grid = QtGui.QGridLayout()
        self.initialize_user_interface()
        self.show()
        QtCore.QTimer.singleShot(10000, self.enter_phase_two)

    def initialize_user_interface(self):
        self.setWindowTitle('Mirror, mirror on the wall')
        self.setWindowIcon(QtGui.QIcon('img/alice_mirror'))
        self.setLayout(self._graphic_grid)
        self._graphic_grid.setSpacing(10)
        # Central items
        for row in range(self._grid.height):
            for col in range(self._grid.width):
                image_path = type_to_image(self._grid[row, col].symbol)
                item_label = ItemLabel(image_path)
                self._graphic_grid.addWidget(item_label, 2 + row, 2 + col)
        self.add_side_buttons()
        self.add_question_marks()
        self.center_on_screen()
        self.resize(1, 1)    # Sets main window to minimal size

    def center_on_screen(self):
        """
           Centers the GUI on the screen.
        """
        window_frame = self.frameGeometry()
        screen_center = QtGui.QDesktopWidget().availableGeometry().center()
        window_frame.moveCenter(screen_center)
        self.move(window_frame.topLeft())

    def erase_items(self):
        """
           Erases mirrors and teleporters from the Gui.
        """
        for row in range(self._grid.height):
            for col in range(self._grid.width):
                empty_label = ItemLabel(type_to_image(' '))
                self._graphic_grid.addWidget(empty_label, 2 + row, 2 + col)

    def add_side_buttons(self):
        """
           Adds exit buttons on all sides of the grid.
        """
        # Top and bottom buttons
        for col in range(self._grid.width):
            top_button = ExitButton('^', -1, col)
            bottom_button = ExitButton('v', self._grid.height, col)
            top_button.setMinimumWidth(1)  # Adapt width to the images
            bottom_button.setMinimumWidth(1)
            self._graphic_grid.addWidget(top_button, 1, 2 + col)
            self._graphic_grid.addWidget(bottom_button,
                                         2 + self._grid.height, 2 + col)
            top_button.clicked.connect(self.button_clicked)
            bottom_button.clicked.connect(self.button_clicked)
        # Left and right buttons
        for row in range(self._grid.height):
            left_button = VerticalExitButton('<', row, -1)
            right_button = VerticalExitButton('>', row, self._grid.width)
            self._graphic_grid.addWidget(left_button, 2 + row, 1)
            self._graphic_grid.addWidget(right_button,
                                         2 + row, 2 + self._grid.width)
            left_button.clicked.connect(self.button_clicked)
            right_button.clicked.connect(self.button_clicked)

    def add_question_marks(self):
        """
           Adds question mark labels on all sides of the grid.
        """
        # Top and bottom labels
        for col in range(self._grid.width):
            top_label = CenteredBoldLabel('?')
            bottom_label = CenteredBoldLabel('?')
            self._graphic_grid.addWidget(top_label, 0, 2 + col,
                                         QtCore.Qt.AlignBottom)
            self._graphic_grid.addWidget(bottom_label,
                                         2 + self._grid.height + 1, 2 + col,
                                         QtCore.Qt.AlignTop)
            self._side_labels += [top_label, bottom_label]
        # Left and right labels
        for row in range(self._grid.height):
            left_label = CenteredBoldLabel('?')
            right_label = CenteredBoldLabel('?')
            self._graphic_grid.addWidget(left_label, 2 + row, 0,
                                         QtCore.Qt.AlignRight)
            self._graphic_grid.addWidget(right_label,
                                         2 + row, 2 + self._grid.width + 1,
                                         QtCore.Qt.AlignLeft)
            self._side_labels += [left_label, right_label]

    def add_laser_label(self):
        """
           Displays the laser initial point as a side label.
        """
        laser_label = CenteredBoldLabel(self._laser.direction)
        if self._laser.direction in ['v', '^']:
            row = (0 if self._laser.direction == 'v'
                   else 2 + self._grid.height + 1)
            self._graphic_grid.addWidget(laser_label, row, 2 + self._laser.y)
        else:
            col = (0 if self._laser.direction == '>'
                   else 2 + self._grid.width + 1)
            self._graphic_grid.addWidget(laser_label, 2 + self._laser.x, col)

    def enter_phase_two(self):
        """
           Erases mirrors and teleporters from the Gui, displays the laser
           entry and activates the gui buttons.
        """
        self.erase_items()
        for label in self._side_labels :
            label.clear()
        self.add_laser_label()
        self._buttons_active = True

    def button_clicked(self):
        """
           Slot called when a button is clicked.
        """
        sender = self.sender()
        if self._buttons_active:
            exit_data = self._grid.compute_all_laser_exits(self._laser)
            message_box = QtGui.QMessageBox()
            if (sender.row, sender.col, sender.text()) in exit_data:
                message_box.setText('Félicitations, vous avez deviné juste !')
            else:
                message_box.setText('Dommage, vous avez perdu !')
                message_box.setInformativeText('Souhaitez-vous proposer une '
                                               'autre sortie ?')
                play_again_button = message_box.addButton(
                                    'Réessayer', QtGui.QMessageBox.AcceptRole)
                message_box.setDefaultButton(play_again_button)
            quit_button = message_box.addButton('Quitter',
                                                QtGui.QMessageBox.RejectRole)
            message_box.exec()
            if message_box.clickedButton() == quit_button:
                self.close()

def type_to_image(type, image_folder=IMAGE_FOLDER):
    """
    :return: The image path corresponding to the given type.
    """
    if type == 'o':
        return image_folder + 'transporter.png'
    elif type == '\\':
        return image_folder + 'back_slash_mirror.png'
    elif type == '/':
        return image_folder + 'forward_slash_mirror.png'
    elif type == '#':
        return image_folder + 'square_mirror.png'
    elif type == '|':
        return image_folder + 'vertical_mirror.png'
    elif type == '-':
        return image_folder + 'horizontal_mirror.png'
    elif type == ' ':
        return image_folder + 'aether.png'
    print("Erreur : type d'objet inconnu.")
    return None

def random_grid(min_height, max_height, min_width, max_width,
                min_items_number, max_items_number):
    """
       Builds a grid object with random size and content.
       The grid contains from min_items_number to max_items_number random
       items, its height ranges from min_height to max_height, and its width
       ranges from min_width to max_width.
       The mirror/teleporter type choice is biased so that it is three times as
       likely to chose a teleporter as any mirror.
    """
    assert conf.min_height <= min_height and max_height <= conf.max_height, \
        "Error : the height range [{}, {}] is not contained in [{}, {}]." \
        .format(min_height, max_height, conf.min_height, conf.max_height)
    assert conf.min_width <= min_width and max_width <= conf.max_width, \
        "Error : the width range [{}, {}] is not contained in [{}, {}]." \
            .format(min_width, max_width, conf.min_width, conf.max_width)
    grid_height = randint(min_height, max_height)
    grid_width = randint(min_width, max_width)
    items_number = randint(min_items_number, max_items_number)
    empty_cells = []
    for row in range(grid_height):
        for col in range(grid_width):
            empty_cells.append((row, col))
    items = []
    for item_number in range(items_number):
        random_cell_number = randint(0, len(empty_cells) - 1)
        random_row, random_col = empty_cells[random_cell_number]
        empty_cells = (empty_cells[:random_cell_number]
                       + empty_cells[random_cell_number + 1:])
        random_type = choice(conf.allowed_items + ['o', 'o'])
        items.append((random_row, random_col,
                      game.build_item(random_row, random_col, random_type)))
    teleporters_count = 0
    for item in items:
        teleporters_count += 1 if item[2].symbol == 'o' else 0
    if teleporters_count == 1:    # Another teleporter is needed
        random_row, random_col = choice(empty_cells)
        items.append((random_row, random_col,
                      game.build_item(random_row, random_col, 'o')))
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

def play():
    _grid = random_grid(MIN_HEIGHT, MAX_HEIGHT, MIN_WIDTH, MAX_WIDTH,
                        MIN_ITEMS_NUMBER, MAX_ITEMS_NUMBER)
    _laser = random_laser(_grid)
    app = QtGui.QApplication(sys.argv)
    game_gui = GameGui(_grid, _laser)
    sys.exit(app.exec_())

if __name__ == '__main__':
    play()
