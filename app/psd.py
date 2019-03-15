from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from app.psd_UI import Ui_PSDWindow

"""
File containing the PSDWindow class, which enable to visualize the PSDs
"""
class PSDWindow(QDialog):
    #=====================================================================
    def __init__(self, epochsPSD, parent=None):
        super(PSDWindow, self).__init__(parent)
        self.psd = epochsPSD
        self.ui = Ui_PSDWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.set_canvas()
        self.set_initial_values()
        self.set_bindings()
        self.plotChange()



    #=====================================================================
    # Setup functions
    def set_initial_values(self) :
        self.ui.epochsSlider.setMaximum(self.psd.data.shape[0] - 1)
        self.ui.fmin.setText(str(self.psd.freqs[0]))
        self.ui.fmax.setText(str(self.psd.freqs[-1]))

    def set_bindings(self) :
        """
        Set Bindings
        """
        self.ui.epochsSlider.valueChanged.connect(self.valueChange)
        self.ui.fmin.editingFinished.connect(self.valueChange)
        self.ui.fmax.editingFinished.connect(self.valueChange)
        self.ui.showMean.stateChanged.connect(self.valueChange)
        self.ui.showSingleEpoch.stateChanged.connect(self.valueChange)
        self.ui.vmax.editingFinished.connect(self.valueChange)
        self.ui.selectPlotType.currentIndexChanged.connect(self.plotChange)

    def set_canvas(self) :
        self.ui.figure = plt.figure(figsize = (10,10))
        self.ui.canvas = FigureCanvas(self.ui.figure)
        # Matplotlib toolbar
        self.ui.toolbar = NavigationToolbar(self.ui.canvas, self)
        self.ui.figureLayout.addWidget(self.ui.canvas)
        self.ui.figureLayout.addWidget(self.ui.toolbar)
    #=====================================================================
    # Plotting function
    def plot_psd(self, epoch_index, f_index_min, f_index_max, vmax) :
        if self.plotType == "Topomap" :
            self.plot_topomaps(epoch_index, f_index_min, f_index_max, vmax)
        if self.plotType == "PSD Matrix" :
            self.plot_matrix(epoch_index, f_index_min, f_index_max, vmax)

    def plot_topomaps(self, epoch_index, f_index_min, f_index_max, vmax):
        """ Plot the topomaps """
        self.ui.figure.clear()
        self.topomaps_adjust(epoch_index, f_index_min, f_index_max, vmax)
        self.add_colorbar([0.915, 0.15, 0.01, 0.7])
        self.ui.figure.subplots_adjust(top = 0.9, right = 0.8, left = 0.1, bottom = 0.1)
        self.ui.canvas.draw()

    def plot_matrix(self, epoch_index, f_index_min, f_index_max, vmax) :
        self.ui.figure.clear()
        self.matrix_adjust(epoch_index, f_index_min, f_index_max, vmax)
        self.add_colorbar([0.915, 0.15, 0.01, 0.7])
        self.ui.figure.subplots_adjust(top = 0.85, right = 0.8, left = 0.1, bottom = 0.1)
        self.ui.canvas.draw()

    def plot_singe_psd(epoch_index, f_index_min, f_index_max) :
        return 0
    #=====================================================================
    # Auxiliary functions for plotting
    def get_index_freq(self, fmin, fmax) :
        """
        Get the indices of the freq between fmin and fmax
        """
        f_index_min, f_index_max = -1, 0
        for freq in self.psd.freqs :
            if freq <= fmin : f_index_min += 1
            if freq <= fmax : f_index_max += 1

        # Just check if f_index_max is not out of bound
        f_index_max = min(len(self.psd.freqs) - 1, f_index_max)
        return f_index_min, f_index_max

    def plotChange(self) :
        """ Update the plot type """
        self.plotType = self.ui.selectPlotType.currentText()
        self.valueChange()

    def valueChange(self) :
        """ Get called if a value is changed """
        fmin = float(self.ui.fmin.text())
        fmax = float(self.ui.fmax.text())
        vmax = float(self.ui.vmax.text())

        f_index_min, f_index_max = self.get_index_freq(fmin ,fmax)
        epoch_index = self.ui.epochsSlider.value()
        self.plot_psd(epoch_index, f_index_min, f_index_max, vmax)

    def topomaps_adjust(self, epoch_index, f_index_min, f_index_max, vmax) :
        """ Plot the good number of subplots and update cbar_image instance"""

        nbFrames = 2 if self.ui.showMean.checkState() and self.ui.showSingleEpoch.checkState() else 1

        # Plot single epoch if showSingleEpoch is checked
        if self.ui.showSingleEpoch.checkState() :
            ax = self.ui.figure.add_subplot(1, nbFrames, 1)
            self.cbar_image, _ = self.psd.plot_topomap_band(epoch_index, f_index_min, f_index_max, axes = ax, vmin = 0, vmax = vmax)
            ax.set_title("Epoch {}".format(epoch_index + 1), fontsize = 15, fontweight = 'light')

        # plot average data if showMean is checked
        if self.ui.showMean.checkState() :
            ax = self.ui.figure.add_subplot(1, nbFrames, nbFrames)
            self.cbar_image, _ = self.psd.plot_avg_topomap_band(f_index_min, f_index_max, axes = ax, vmin = 0, vmax = vmax)
            ax.set_title("Average", fontsize = 15, fontweight = 'light')

    def matrix_adjust(self, epoch_index, f_index_min, f_index_max, vmax) :
        """Plot the matrix and update cbar_image instance """
        nbFrames = 2 if self.ui.showMean.checkState() and self.ui.showSingleEpoch.checkState() else 1

        # plot single epoch data uf showSingleEpoch is checked
        if self.ui.showSingleEpoch.checkState() :
            ax = self.ui.figure.add_subplot(1, nbFrames, 1)
            self.cbar_image = self.psd.plot_matrix(epoch_index, f_index_min, f_index_max, axes = ax, vmin = 0, vmax = vmax)
            ax.axis('tight')
            ax.set_title("PSD Matrix for epoch {}".format(epoch_index + 1), fontsize = 15, fontweight = 'light')
            ax.set_xlabel('Frequencies (Hz)')
            ax.set_ylabel('Channels')
            ax.xaxis.set_ticks_position('bottom')

        # plot average data if showMean is checked
        if self.ui.showMean.checkState() :
            ax = self.ui.figure.add_subplot(1, nbFrames, nbFrames)
            self.cbar_image = self.psd.plot_avg_matrix(f_index_min, f_index_max, axes = ax, vmin = 0, vmax = vmax)
            ax.axis('tight')
            ax.set_title("Average PSD Matrix", fontsize = 15, fontweight = 'light')
            ax.set_xlabel('Frequencies (Hz)')
            ax.set_ylabel('Channels')
            ax.xaxis.set_ticks_position('bottom')

    def add_colorbar(self, position) :
        """ Add colorbar to the plot at position """
        if self.ui.showSingleEpoch.checkState() or self.ui.showMean.checkState() :
            # plot a common colorbar for both representations
            cax = self.ui.figure.add_axes(position)
            cbar = plt.colorbar(self.cbar_image, cax = cax)
            cbar.ax.get_xaxis().labelpad = 15
            cbar.ax.set_xlabel('PSD (µV²/Hz)')
