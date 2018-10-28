from PyQt4 import QtGui, QtCore

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

class VExitButton(ExitButton):
    """
       A vertical exit button on the left or right side of the grid.
       Its width is fixed to the default height of a QPushButton.
    """
    def __init__(self, text, row, col):
        super().__init__(text, row, col)
        self.setSizePolicy(QtGui.QSizePolicy.Fixed,
                           QtGui.QSizePolicy.Expanding)
        self.setFixedWidth(QtGui.QPushButton().sizeHint().height())

class HExitButton(ExitButton):
    """
       A horizontal exit button on the top or bottom side of the grid.
       Its width can take any value to adjust to the size of the images.
    """
    def __init__(self, text, row, col):
        super().__init__(text, row, col)
        self.setMinimumWidth(1)

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
    """
    def __init__(self, image_path):
        super().__init__()
        self.setPixmap(QtGui.QPixmap(image_path))
        self.setScaledContents(True)