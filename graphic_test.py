import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QSlider, QLabel, QLineEdit, QCheckBox
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
                             n_fft = 512, n_per_seg = 30, n_overlap = 15)

        # a figure instance to plot on
        self.figure = plt.figure(figsize = (10,5))
        # Canvas
        self.canvas = FigureCanvas(self.figure)
        # Matplotlib toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Frequency lines
        self.fminLabel = QLabel('Min Frequency (Hz):', self)
        self.fmin = QLineEdit()
        self.fmin.setValidator(QIntValidator())
        self.fmin.setMaxLength(4)
        self.fmin.setText("10")

        self.fmaxLabel = QLabel('Max Frequency (Hz):', self)
        self.fmax = QLineEdit()
        self.fmax.setValidator(QIntValidator())
        self.fmax.setMaxLength(4)
        self.fmax.setText("20")

        # Epochs
        self.epochsLabel = QLabel('Epoch:', self)
        self.epochsSl = QSlider(Qt.Horizontal)
        self.epochsSl.setFocusPolicy(Qt.StrongFocus)
        self.epochsSl.setTickPosition(QSlider.TicksBelow)
        self.epochsSl.setMaximum(self.psd.data.shape[0] - 1)
        self.epochsSl.setMinimum(0)
        self.epochsSl.setValue(0)
        self.epochsSl.setTickInterval(1)

        # Show mean of epochs
        self.showMean = QCheckBox('Show Average over Epochs', self)

        # Value maximum of the amplitude
        self.vminLabel = QLabel('Scaling for amplitude (µV / m²):', self)
        self.vmin = QLineEdit()
        self.vmin.setValidator(QDoubleValidator())
        self.vmin.setMaxLength(15)
        self.vmin.setText("1e-12")


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
        layout.addWidget(self.showMean)

        layout.addWidget(self.vminLabel)
        layout.addWidget(self.vmin)
        self.setLayout(layout)

        self.epochsSl.valueChanged.connect(self.valueChange)
        self.fmin.editingFinished.connect(self.valueChange)
        self.fmax.editingFinished.connect(self.valueChange)
        self.showMean.stateChanged.connect(self.valueChange)
        self.vmin.editingFinished.connect(self.valueChange)

        self.valueChange()

    def valueChange(self) :
        fmin = int(self.fmin.text())
        fmax = int(self.fmax.text())
        vmax = float(self.vmin.text())

        # Simple iteration on psd.freqs to get all the index for frequencies within this range
        f_index_min, f_index_max = -1, 0
        for freq in self.psd.freqs :
            if freq <= fmin : f_index_min += 1
            if freq <  fmax : f_index_max += 1

        epoch_index = self.epochsSl.value()
        self.plot_maps(epoch_index, f_index_min, f_index_max, vmax)

    def plot_maps(self, epoch_index, f_index_min, f_index_max, vmax):
        ''' Plot the topomap'''
        fmin = self.psd.freqs[f_index_min]
        fmax = self.psd.freqs[f_index_max]
        # instead of ax.hold(False)
        self.figure.clear()
        self.figure.suptitle('Frequency band {:.2f} to {:.2f} Hz'.format(fmin ,fmax),
                     fontsize = 20, fontweight = 'bold')

        nbFrames = 2 if self.showMean.checkState() else 1

        # plot data of the selected epoch
        ax = self.figure.add_subplot(1, nbFrames, 1)
        image, _ = self.psd.plot_topomap_band(epoch_index, f_index_min, f_index_max, axes = ax, vmin = 0, vmax = vmax)
        ax.set_title("Epoch {}".format(epoch_index + 1), fontsize = 15, fontweight = 'light')

        # plot average data if showMean is checked
        if self.showMean.checkState() :
            ax = self.figure.add_subplot(1, nbFrames, 2)
            self.psd.plot_avg_topomap_band(f_index_min, f_index_max, axes = ax, vmin = 0, vmax = vmax)
            ax.set_title("Average", fontsize = 15, fontweight = 'light')

        # plot a common colorbar for both representations
        cax = self.figure.add_axes([0.915, 0.15, 0.01, 0.7])
        plt.colorbar(image, cax = cax)
        self.figure.subplots_adjust(top = 0.8, right = 0.8, left = 0.1, bottom = 0.1)

        # refresh canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
