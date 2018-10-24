import sys
from PyQt4 import QtGui
from random import randint, choice
import conf

def random_grid():
    """
       Builds a grid object with random items.
       The number of random items is set to be slightly less than the square
       root of the number of cells in the grid.
    """
    grid_height = randint(3, 26)
    grid_width = randint(3, 26)
    average = int((grid_height*grid_width)**(1/2))
    nb_items = randint(average - 2, average + 2)
    # List of all possible coordinates
    coordinates = list(zip([i for i in range(grid_height)],
                           [j for j in range(grid_width)]))
    items = []
    for k in range(nb_items):
        random_coordinates = choice(coordinates)
        coordinates
        random_type = choice(conf.allowed_items)
        items.append(())


class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        title = QtGui.QLabel('Title')
        author = QtGui.QLabel('Author')
        review = QtGui.QLabel('Review')

        titleEdit = QtGui.QLineEdit()
        authorEdit = QtGui.QLineEdit()
        reviewEdit = QtGui.QTextEdit()

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)

        self.setLayout(grid)

        # self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Review')
        self.show()


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    random_grid()