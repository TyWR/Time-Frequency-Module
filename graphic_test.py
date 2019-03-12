import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QSlider, QLabel, QLineEdit
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from example_data import get_epochs
from processing import EpochsPSD


class Window(QDialog):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # Dataset
        self.epochs = get_epochs()
        self.psd = EpochsPSD(self.epochs, fmin = 0, fmax = 75, tmin = 0, tmax = 0.5, method = 'welch',
                             n_fft = 256, n_per_seg = 30, n_overlap = 15)

        # a figure instance to plot on
        self.figure = plt.figure()
        # Canvas
        self.canvas = FigureCanvas(self.figure)
        # Matplotlib toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Frequency lines
        self.fminLabel = QLabel('Min Frequency :', self)
        self.fmin = QLineEdit()
        self.fmin.setValidator(QIntValidator())
        self.fmin.setMaxLength(4)

        self.fmaxLabel = QLabel('Max Frequency :', self)
        self.fmax = QLineEdit()
        self.fmax.setValidator(QIntValidator())
        self.fmax.setMaxLength(4)


        # Epochs
        self.epochsLabel = QLabel('Epoch:', self)
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

        layout.addWidget(self.fminLabel)
        layout.addWidget(self.fmin)

        layout.addWidget(self.fmaxLabel)
        layout.addWidget(self.fmax)

        layout.addWidget(self.epochsLabel)
        layout.addWidget(self.epochsSl)
        self.setLayout(layout)

        self.epochsSl.valueChanged.connect(self.valueChange)
        self.fmin.editingFinished.connect(self.valueChange)
        self.fmax.editingFinished.connect(self.valueChange)



    def valueChange(self) :
        fmin = int(self.fmin.text())
        fmax = int(self.fmax.text())

        # Simple iteration on psd.freqs to get all the index for frequencies within this range
        f_index_min, f_index_max = -1, 0
        for freq in self.psd.freqs :
            if freq <= fmin : f_index_min += 1
            if freq <  fmax : f_index_max += 1

        epoch_index = self.epochsSl.value()
        self.plot(epoch_index, f_index_min, f_index_max)


    def plot(self, epoch_index, f_index_min, f_index_max):
        ''' Plot the topomap'''
        # instead of ax.hold(False)
        self.figure.clear()
        # create an axis
        ax = self.figure.add_subplot(111)
        # plot data
        self.psd.plot_topomap_band_frequency(epoch_index, f_index_min, f_index_max, axes = ax)
        ax.set_title("Map of the power for the frequency band [{:.2f}, {:.2f}]".format(
                     self.psd.freqs[f_index_min], self.psd.freqs[f_index_max]))
        # refresh canvas
        self.canvas.draw()




if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
