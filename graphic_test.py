import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import random

from example_data import get_epochs
from processing import EpochsPSD


class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.epochs = get_epochs()
        self.psd = EpochsPSD(self.epochs, fmin = 0, fmax = 50, tmin = 0, tmax = 0.5, method = 'multitaper', bandwidth = 4)

        # a figure instance to plot on
        self.figure = plt.figure()

        # Canvas
        self.canvas = FigureCanvas(self.figure)

        # Matplotlib toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.freqLabel = QLabel('Frequencies:', self)
        self.epochsLabel = QLabel('Epoch:', self)

        # Add a Slider for frequencies
        self.freqSl = QSlider(Qt.Horizontal)
        self.freqSl.setFocusPolicy(Qt.StrongFocus)
        self.freqSl.setTickPosition(QSlider.TicksBelow)
        self.freqSl.setMaximum(len(self.psd.freqs)-1)
        self.freqSl.setMinimum(0)
        self.freqSl.setValue(0)
        self.freqSl.setTickInterval(1)

        # Add a Slider for epochs
        self.epochsSl = QSlider(Qt.Horizontal)
        self.epochsSl.setFocusPolicy(Qt.StrongFocus)
        self.epochsSl.setTickPosition(QSlider.TicksBelow)
        self.epochsSl.setMaximum(self.psd.data.shape[0] - 1)
        self.epochsSl.setMinimum(0)
        self.epochsSl.setValue(0)
        self.epochsSl.setTickInterval(1)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.freqLabel)
        layout.addWidget(self.freqSl)
        layout.addWidget(self.epochsLabel)
        layout.addWidget(self.epochsSl)
        self.setLayout(layout)

        self.freqSl.valueChanged.connect(self.valueChange)
        self.epochsSl.valueChanged.connect(self.valueChange)


    def valueChange(self) :
        freq_index = self.freqSl.value()
        epoch_index = self.epochsSl.value()
        self.plot(epoch_index, freq_index)


    def plot(self, epoch_index, freq_index):
        ''' Plot the topomap'''
        # instead of ax.hold(False)
        self.figure.clear()
        # create an axis
        ax = self.figure.add_subplot(111)
        # plot data
        self.psd.plot_map_epoch(epoch_index, freq_index, axes = ax)
        ax.set_title("Map of the power for the frequency {}".format(self.psd.freqs[freq_index]))
        # refresh canvas
        self.canvas.draw()




if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
