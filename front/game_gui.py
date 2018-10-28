from PyQt4 import QtGui, QtCore
import front.widgets as widgets
import front.front_utils as front_utils
import back.laser as laser
import conf

class GameGui(QtGui.QWidget):
    """
       The main graphic user interface, consisting of a grid filled with
       mirrors and teleporters, as well as buttons on the sides for the player
       to guess a laser exit.
       The buttons only activate after a set time.
       All labels are kept in memory to be able to clear them.
    """
    def __init__(self, _grid, _laser):
        super().__init__()
        self._grid = _grid
        self._laser = _laser
        _laser_copy = laser.Laser(_laser.x, _laser.y, _laser.direction, _grid)
        self._solution = self._grid.compute_all_laser_exits(_laser_copy)
        self._buttons_active = False
        self._side_labels = []
        self._laser_label = QtGui.QLabel()
        self._graphic_grid = QtGui.QGridLayout()
        self.initialize_user_interface()
        QtCore.QTimer.singleShot(conf.phase_one_duration, self.enter_phase_two)

    def initialize_user_interface(self):
        self.setWindowTitle(conf.game_name)
        self.setWindowIcon(QtGui.QIcon('img/alice_mirror'))
        self.setLayout(self._graphic_grid)
        self.add_items_labels()
        self.add_question_marks()
        self.add_side_buttons()
        self.center_on_screen()
        self.resize(1, 1)  # Sets main window to minimal size
        self.show()

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
                empty_label = widgets.ItemLabel(front_utils.path_to_image(' '))
                self._graphic_grid.addWidget(empty_label, 2 + row, 2 + col)

    def add_items_labels(self):
        """
           Adds mirrors and teleporters labels in the grid.
        """
        for row in range(self._grid.height):
            for col in range(self._grid.width):
                item_label = widgets.ItemLabel(front_utils.path_to_image(
                                               self._grid[row, col].symbol))
                self._graphic_grid.addWidget(item_label, 2 + row, 2 + col)

    def add_side_buttons(self):
        """
           Adds exit buttons on all sides of the grid.
        """
        # Top and bottom buttons
        for col in range(self._grid.width):
            top_button = widgets.HExitButton('^', -1, col)
            bottom_button = widgets.HExitButton('v', self._grid.height, col)
            self._graphic_grid.addWidget(top_button, 1, 2 + col)
            self._graphic_grid.addWidget(bottom_button,
                                         2 + self._grid.height, 2 + col)
            top_button.clicked.connect(self.button_clicked)
            bottom_button.clicked.connect(self.button_clicked)
        # Left and right buttons
        for row in range(self._grid.height):
            left_button = widgets.VExitButton('<', row, -1)
            right_button = widgets.VExitButton('>', row, self._grid.width)
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
            top_label = widgets.CenteredBoldLabel('?')
            bottom_label = widgets.CenteredBoldLabel('?')
            self._graphic_grid.addWidget(top_label, 0, 2 + col,
                                         QtCore.Qt.AlignBottom)
            self._graphic_grid.addWidget(bottom_label,
                                         2 + self._grid.height + 1, 2 + col,
                                         QtCore.Qt.AlignTop)
            self._side_labels += [top_label, bottom_label]
        # Left and right labels
        for row in range(self._grid.height):
            left_label = widgets.CenteredBoldLabel('?')
            right_label = widgets.CenteredBoldLabel('?')
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
        laser_label = widgets.CenteredBoldLabel(self._laser.direction)
        if self._laser.direction in ['v', '^']:
            row = (0 if self._laser.direction == 'v'
                   else 2 + self._grid.height + 1)
            self._graphic_grid.addWidget(laser_label, row, 2 + self._laser.y)
        else:
            col = (0 if self._laser.direction == '>'
                   else 2 + self._grid.width + 1)
            self._graphic_grid.addWidget(laser_label, 2 + self._laser.x, col)
        self._laser_label = laser_label

    def enter_phase_two(self):
        """
           Erases mirrors and teleporters from the Gui, displays the laser
           initial state and activates the gui buttons.
        """
        self.erase_items()
        for label in self._side_labels :
            label.clear()
        self.add_laser_label()
        self._buttons_active = True

    def reset_game(self):
        """
           Reverts the Gui to its initial state.
        """
        self._buttons_active = False
        self._laser_label.clear()
        self.add_items_labels()
        self.add_question_marks()
        QtCore.QTimer.singleShot(conf.second_display_duration,
                                 self.enter_phase_two)

    def button_clicked(self):
        """
           Slot called when a button is clicked.
        """
        sender = self.sender()
        if self._buttons_active:
            message_box = QtGui.QMessageBox()
            quit_button = message_box.addButton('Quitter',
                                                QtGui.QMessageBox.RejectRole)
            if (sender.row, sender.col, sender.text()) in self._solution:
                message_box.setText('Félicitations, vous avez deviné juste !')
            else:
                message_box.setText('Dommage, vous avez perdu !')
                message_box.setInformativeText('Vous pouvez proposer une '
                                               'autre sortie, ou afficher de '
                                               'nouveau les objets.')
                show_items_button = message_box.addButton('Voir objets',
                                    QtGui.QMessageBox.AcceptRole)
                play_again_button = message_box.addButton( 'Réessayer',
                                    QtGui.QMessageBox.AcceptRole)
                message_box.setDefaultButton(play_again_button)
            message_box.exec()
            if message_box.clickedButton() == quit_button:
                self.close()
            elif message_box.clickedButton() == show_items_button:
                self.reset_game()