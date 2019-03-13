from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


"""
File containing the PSDWindow class, which enable to visualize the PSDs
"""
class PSDWindow(QDialog):

    def __init__(self, epochsPSD, parent=None):
        super(PSDWindow, self).__init__(parent)

        # Dataset
        self.psd = epochsPSD

        # a figure instance to plot on
        self.figure = plt.figure(figsize = (10,10))
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

        # Show single Epoch
        self.showSingleEpoch = QCheckBox('Show Single Epoch', self)

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
        self.showMean.setCheckState(2)

        # Value maximum of the amplitude
        self.vminLabel = QLabel('Scaling for amplitude (µV² / Hz):', self)
        self.vmin = QLineEdit()
        self.vmin.setValidator(QDoubleValidator())
        self.vmin.setMaxLength(15)
        self.vmin.setText("3e-12")

        # Recap of the parameters
        self.parameters = QLabel(epochsPSD.__str__())

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        layout.addWidget(self.fminLabel)
        layout.addWidget(self.fmin)

        layout.addWidget(self.fmaxLabel)
        layout.addWidget(self.fmax)

        layout.addWidget(self.showSingleEpoch)
        layout.addWidget(self.epochsLabel)
        layout.addWidget(self.epochsSl)
        layout.addWidget(self.showMean)

        layout.addWidget(self.vminLabel)
        layout.addWidget(self.vmin)

        layout.addWidget(self.parameters)
        self.setLayout(layout)

        self.epochsSl.valueChanged.connect(self.valueChange)
        self.fmin.editingFinished.connect(self.valueChange)
        self.fmax.editingFinished.connect(self.valueChange)
        self.showMean.stateChanged.connect(self.valueChange)
        self.showSingleEpoch.stateChanged.connect(self.valueChange)
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
            if freq <= fmax : f_index_max += 1

        # Just check if f_index_max is not out of bound
        f_index_max = min(len(self.psd.freqs) - 1, f_index_max)

        epoch_index = self.epochsSl.value()
        self.plot_maps(epoch_index, f_index_min, f_index_max, vmax)

    def plot_maps(self, epoch_index, f_index_min, f_index_max, vmax):
        ''' Plot the topomap'''
        fmin = self.psd.freqs[f_index_min]
        fmax = self.psd.freqs[f_index_max]

        self.figure.clear()
        self.figure.suptitle('Frequency band {:.2f} to {:.2f} Hz'.format(fmin ,fmax),
                     fontsize = 20, fontweight = 'bold')

        # Plot 2 topomaps if showMean is checked, one otherwise
        both = self.showMean.checkState() and self.showSingleEpoch.checkState()
        nbFrames = 2 if both else 1

        if self.showSingleEpoch.checkState() :
            # plot data of the selected epoch
            ax = self.figure.add_subplot(1, nbFrames, 1)
            image, _ = self.psd.plot_topomap_band(epoch_index, f_index_min, f_index_max, axes = ax, vmin = 0, vmax = vmax)
            ax.set_title("Epoch {}".format(epoch_index + 1), fontsize = 15, fontweight = 'light')

        # plot average data if showMean is checked
        if self.showMean.checkState() :
            ax = self.figure.add_subplot(1, nbFrames, nbFrames)
            image, _ = self.psd.plot_avg_topomap_band(f_index_min, f_index_max, axes = ax, vmin = 0, vmax = vmax)
            ax.set_title("Average", fontsize = 15, fontweight = 'light')

        if self.showSingleEpoch.checkState() or self.showMean.checkState() :
            # plot a common colorbar for both representations
            cax = self.figure.add_axes([0.915, 0.15, 0.01, 0.7])
            cbar = plt.colorbar(image, cax = cax)
            cbar.ax.get_xaxis().labelpad = 15
            cbar.ax.set_xlabel('PSD (µV²/Hz)')
            self.figure.subplots_adjust(top = 0.8, right = 0.8, left = 0.1, bottom = 0.1)

        # refresh canvas
        self.canvas.draw()
