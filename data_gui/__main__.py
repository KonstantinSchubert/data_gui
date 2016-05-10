from PyQt4 import QtGui
from gui import ApplicationWindow
import os
import sys

progversion = "0.1"


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    qApp = QtGui.QApplication(sys.argv)

    aw = ApplicationWindow()
    if args != []: # a filename was passed
        aw.openFile(args[0])
    aw.setWindowTitle("Data GUI")
    aw.show()
    sys.exit(qApp.exec_())

if __name__ == "__main__":
    main()
