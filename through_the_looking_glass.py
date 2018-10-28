import sys
from PyQt4 import QtGui
import conf
import front.creation_tools as creation_tools
import front.game_gui as game_gui

def play():
    _grid = creation_tools.random_grid(conf.min_random_height,
                                       conf.max_random_height,
                                       conf.min_random_width,
                                       conf.max_random_width,
                                       conf.min_random_items,
                                       conf.max_random_items)
    _laser = creation_tools.random_laser(_grid)
    app = QtGui.QApplication(sys.argv)
    _game_gui = game_gui.GameGui(_grid, _laser)
    sys.exit(app.exec_())

if __name__ == '__main__':
    play()
