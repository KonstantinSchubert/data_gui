#!/usr/bin/env python


from __future__ import unicode_literals
import sys
import os
import re
import random
from PyQt4 import QtGui, QtCore
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import dataframe_managers
import numpy as np

progname = os.path.basename(sys.argv[0])
progversion = "0.1"


class PlotCanvas(FigureCanvasQTAgg):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        FigureCanvasQTAgg.__init__(self, fig)
        self.setParent(parent)

        FigureCanvasQTAgg.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)


    def update_figure(self, dataFrame, vars):
        # for now, let's plot only one variable
        var = vars[0]
        array_to_plot = dataFrame[var].values
        self.axes.hist(array_to_plot, bins=50)
        self.draw()

class ApplicationWindow(QtGui.QMainWindow):



    def update_plot(self):

        def get_variables_plotstring():
            plotstring = str(self.variables_to_plot.text())
            variable_list = plotstring.split(":")
            return variable_list

        def get_cutstring():
            cut = str(self.cutstring.text())
            return cut

        def get_variables_cutstring():
            cut = get_cutstring()
            logical_expressions = ["and", "or", "&","|","(",")","<",">","=","True","False"," "]
            for expression in logical_expressions:
                cut = cut.replace(expression, ",")
            variables = cut.split(",")
            regex = re.compile('[-+]?[0-9]+\.?[0-9]*') # match any signed number
            variables = [x for x in variables if not (x == "" or regex.match(x)) ]
            return variables

        if self.dataFrameManager is None:
            # no file is open, so we return
            return
        available_variables = self.dataFrameManager.get_all_columns()
        needed_variables = list(set(get_variables_plotstring() + get_variables_cutstring()))
        all_exist = np.all([(var in available_variables) for var in needed_variables])
        if not all_exist:
            #todo: better notification
            self.statusBar().showMessage("Variables or cutstring invalid", 2000)
        else:
            #todo: better notification
            self.statusBar().showMessage("Loading dataset...", 2000)
            cutstring = get_cutstring()
            if cutstring=="":
                cutstring = None
            try:
                df = self.dataFrameManager.get_DataFrame(columns=needed_variables, query=cutstring)
                self.plot_canvas.update_figure(dataFrame=df, vars=get_variables_plotstring())
            except (KeyError, TypeError, SyntaxError, ValueError) as e:
                # we catch all kinds or errors which are mostly caused by invalid query strings
                # unfortunately even valid query strings seem to fail
                self.statusBar().showMessage("Bad Query String?", 2000)
                return
            self.statusBar().showMessage("Success", 2000)

            




    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("Pandas Gui")

        self.file_menu = QtGui.QMenu('&File', self)
        self.file_menu.addAction('&Open', self.openFile, QtCore.Qt.CTRL + QtCore.Qt.Key_O)
        self.file_menu.addAction('&Quit', self.fileQuit, QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.dataFrameManager = None



        self.main_widget = QtGui.QWidget(self)

        #########
        # sidebar
        #########
        queryLabel = QtGui.QLabel("Search:");
        queryEdit = QtGui.QLineEdit();
        self.variables_view = QtGui.QListView();
        self.variables_model = QtGui.QStringListModel(self.main_widget)
        proxy = QtGui.QSortFilterProxyModel(self.main_widget)
        proxy.setSourceModel(self.variables_model)
        self.variables_view.setModel(proxy)


        QtCore.QObject.connect(queryEdit, QtCore.SIGNAL("textChanged(QString)"), 
                proxy, QtCore.SLOT("setFilterFixedString(QString)"))

        queryLayout = QtGui.QHBoxLayout()
        queryLayout.addWidget(queryLabel)
        queryLayout.addWidget(queryEdit)

        sidebar = QtGui.QVBoxLayout()
        sidebar.addLayout(queryLayout)
        sidebar.addWidget(self.variables_view)

        ###########
        # main view
        ###########


        self.variables_to_plot = QtGui.QLineEdit(text=" (todo:use tags like on SO)", parent=self.main_widget)
        self.cutstring = QtGui.QLineEdit(parent=self.main_widget)


        strings = QtGui.QVBoxLayout()
        strings.addWidget(self.variables_to_plot)
        strings.addWidget(self.cutstring)

        labels = QtGui.QVBoxLayout()
        labels.addWidget(QtGui.QLabel("Variable(s)"))
        labels.addWidget(QtGui.QLabel("Query"))


        stringbox = QtGui.QHBoxLayout()
        stringbox.addLayout(labels)
        stringbox.addLayout(strings)

        self.plot_canvas = PlotCanvas(self.main_widget, width=5, height=4, dpi=100)        
        bigview = QtGui.QVBoxLayout()
        bigview.addLayout(stringbox)
        bigview.addWidget(self.plot_canvas)

        
        
        #########################
        # putting it all together
        #########################
        main_layout = QtGui.QHBoxLayout(self.main_widget)
        main_layout.addLayout(sidebar);
        main_layout.addLayout(bigview)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        ##############
        # Wiring it up
        ##############
        QtCore.QObject.connect(self.variables_to_plot, QtCore.SIGNAL("textChanged(QString)"), 
                               self.update_plot)
        QtCore.QObject.connect(self.cutstring, QtCore.SIGNAL("textChanged(QString)"), 
                               self.update_plot)


    def openFile(self):
        file_name = QtGui.QFileDialog.getOpenFileName(
                                        self.main_widget,
                                        "Open Image", os.path.expanduser('~'),
                                        "Data Files (*.root)");
        if file_name[-5:] == ".root":
            self.dataFrameManager = dataframe_managers.DataFrameManagerROOT(str(file_name))
        else:
            raise Exception("Cannot open this file type. TODO: Just inform the user instead of crashing.")

        columns = self.dataFrameManager.get_all_columns()
        self.variables_model.setStringList(columns)

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
