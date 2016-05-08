#!/usr/bin/env python


from __future__ import unicode_literals
import sys
import os
import random
from PyQt4 import QtGui, QtCore
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import dataframe_managers

progname = os.path.basename(sys.argv[0])
progversion = "0.1"


class MyMplCanvas(FigureCanvasQTAgg):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvasQTAgg.__init__(self, fig)
        self.setParent(parent)

        FigureCanvasQTAgg.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class PlotCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(10000)

    def compute_initial_figure(self):
        pass

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]

        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()


class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("Pandas Gui")

        self.file_menu = QtGui.QMenu('&File', self)
        self.file_menu.addAction('&Open', self.openFile, QtCore.Qt.CTRL + QtCore.Qt.Key_O)
        self.file_menu.addAction('&Quit', self.fileQuit, QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.dataFrameManager = None

        # self.help_menu = QtGui.QMenu('&Help', self)
        # self.menuBar().addSeparator()
        # self.menuBar().addMenu(self.help_menu)

        # self.help_menu.addAction('&About', self.about)



        self.main_widget = QtGui.QWidget(self)

        # sidebar
        queryLabel = QtGui.QLabel("Search:");
        queryEdit = QtGui.QLineEdit();
        filtered_available_vars = QtGui.QTableView(); # better use list view here

        queryLayout = QtGui.QHBoxLayout();
        queryLayout.addWidget(queryLabel);
        queryLayout.addWidget(queryEdit);

        sidebar = QtGui.QVBoxLayout();
        sidebar.addLayout(queryLayout);
        sidebar.addWidget(filtered_available_vars);


        # main view
        bigview = QtGui.QVBoxLayout();
        variables_to_plot = QtGui.QLineEdit(text="here go variables to plot like tags on SO", parent=self.main_widget)
        cutstring = QtGui.QLineEdit(text="here goes cutstring as text", parent=self.main_widget)
        plot_canvas = PlotCanvas(self.main_widget, width=5, height=4, dpi=100)
        bigview.addWidget(variables_to_plot)
        bigview.addWidget(cutstring)
        bigview.addWidget(plot_canvas)
        
        
        # putting it all together
        main_layout = QtGui.QHBoxLayout(self.main_widget)
        main_layout.addLayout(sidebar);
        main_layout.addLayout(bigview)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("By Konstantin Schubert!", 2000)

    def openFile(self):
        file_name = QtGui.QFileDialog.getOpenFileName(
                                        self.main_widget,
                                        "Open Image", os.path.expanduser('~'),
                                        "Data Files (*.root)");
        if file_name[-5:] == ".root":
            self.dataFrameManager = dataframe_managers.DataFrameManagerROOT(file_name)
        else:
            raise Exception("Cannot open this file type. TODO: Just inform the user instead of crashing.")

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()



qApp = QtGui.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()
