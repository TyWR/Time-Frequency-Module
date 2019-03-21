from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from math import floor


from app.raw_psd_UI import Ui_RawPSDWindow

class RawPSDWindow(QDialog):
    def __init__(self, rawPSD, parent=None):
        super(RawPSDWindow, self).__init__(parent)
        self.psd = rawPSD
        self.ui = Ui_RawPSDWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.setup_window()

    #---------------------------------------------------------------------
    def setup_window(self) :
        self.set_canvas()
        self.set_initial_values()
        self.set_bindings()
        self.plot_change()

    #=====================================================================
    # Setup functions
    #=====================================================================
    def set_initial_values(self) :
        """Setup initial values"""
        self.ui.fmin.setText(str(self.psd.freqs[0]))
        self.ui.fmin.setMaxLength(4)
        self.ui.fmax.setText(str(self.psd.freqs[-1]))
        self.ui.fmin.setMaxLength(4)
        self.ui.vmax.setText("0")   #Auto scaling by default
        self.ui.fmin.setMaxLength(6)
        self.ui.selectPlotType.addItem("PSD Matrix")
        self.ui.selectPlotType.addItem("Topomap")

    #---------------------------------------------------------------------
    def set_bindings(self) :
        """Set Bindings"""
        self.ui.fmin.editingFinished.connect(self.value_change)
        self.ui.fmax.editingFinished.connect(self.value_change)
        self.ui.vmax.editingFinished.connect(self.value_change)
        self.ui.selectPlotType.currentIndexChanged.connect(self.plot_change)

    #---------------------------------------------------------------------
    def set_canvas(self) :
        """setup canvas for matplotlib"""
        self.ui.figure = plt.figure(figsize = (10,10))
        self.ui.canvas = FigureCanvas(self.ui.figure)
        cid = self.ui.canvas.mpl_connect('button_press_event', self.__onclick__)
        self.cursor = ()
        # Matplotlib toolbar
        self.ui.toolbar = NavigationToolbar(self.ui.canvas, self)
        self.ui.figureLayout.addWidget(self.ui.canvas)
        self.ui.figureLayout.addWidget(self.ui.toolbar)

    #=====================================================================
    # Main Plotting function
    #=====================================================================
    def plot_psd(self, f_index_min, f_index_max, vmax) :
        """Plot the correct type of PSD"""
        if self.plotType == "Topomap" :
            self.plot_topomap(f_index_min, f_index_max, vmax)
        if self.plotType == "PSD Matrix" :
            self.plot_matrix(f_index_min, f_index_max, vmax)

    #---------------------------------------------------------------------
    def plot_topomap(self, f_index_min, f_index_max, vmax):
        """Plot the topomaps"""
        self.ui.figure.clear()
        ax = self.ui.figure.add_subplot(1, 1, 1)
        self.cbar_image, _ = self.psd.plot_topomap_band(f_index_min, f_index_max, axes = ax, vmin = 0, vmax = vmax)
        self.add_colorbar([0.915, 0.15, 0.01, 0.7])
        self.ui.figure.subplots_adjust(top = 0.9, right = 0.8, left = 0.1, bottom = 0.1)
        self.ui.canvas.draw()

    #---------------------------------------------------------------------
    def plot_matrix(self, f_index_min, f_index_max, vmax) :
        """Plot the PSD Matrix"""
        self.ui.figure.clear()
        ax = self.ui.figure.add_subplot(1, 1, 1)
        self.cbar_image = self.psd.plot_matrix(f_index_min, f_index_max, axes = ax, vmin = 0, vmax = vmax)
        ax.axis('tight')
        ax.set_title("PSD Matrix", fontsize = 15, fontweight = 'light')
        ax.set_xlabel('Frequencies (Hz)')
        ax.set_ylabel('Channels')
        ax.xaxis.set_ticks_position('bottom')
        self.add_colorbar([0.915, 0.15, 0.01, 0.7])
        self.ui.figure.subplots_adjust(top = 0.85, right = 0.8, left = 0.1, bottom = 0.1)
        self.ui.canvas.draw()

    #=====================================================================
    # Handle PSD single plotting on click
    #=====================================================================
    def __onclick__(self, click) :
        """Get coordinates on the canvas and plot the corresponding PSD"""
        channel_picked = click.ydata

        if channel_picked is not None and self.plotType == "PSD Matrix" and click.dblclick :
            channel_picked = floor(channel_picked)
            self.plot_single_psd(channel_picked, channel_picked)

    #---------------------------------------------------------------------
    def plot_single_psd(self, epoch_picked, channel_picked) :
        """Plot one single PSD"""
        plt.close('all')
        fig = plt.figure(figsize = (5, 5))
        ax = fig.add_subplot(1, 1, 1)
        self.psd.plot_single_psd(channel_picked - 1, self.f_index_min, self.f_index_max, axes = ax)
        ax.set_title('PSD of channel {}'.format(channel_picked))
        self.set_ax_single_psd(ax)

    #=====================================================================
    # Adjusting the plots
    #=====================================================================
    def add_colorbar(self, position) :
        """ Add colorbar to the plot at correct position """
        cax = self.ui.figure.add_axes(position)
        cbar = plt.colorbar(self.cbar_image, cax = cax)
        cbar.ax.get_xaxis().labelpad = 15
        cbar.ax.set_xlabel('PSD (µV²/Hz)')

    #---------------------------------------------------------------------
    def set_ax_single_psd(self, ax) :
        """Set axes values for a single PSD plot"""
        ax.set_xlim([self.psd.freqs[self.f_index_min], self.psd.freqs[self.f_index_max]])
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Power (µV²/Hz)')
        plt.show()

    #=====================================================================
    # Updating the canvas functions
    #=====================================================================
    def plot_change(self) :
        """Update the plot type"""
        self.plotType = self.ui.selectPlotType.currentText()
        self.value_change()

    #---------------------------------------------------------------------
    def value_change(self) :
        """ Get called if a value is changed """
        fmin = float(self.ui.fmin.text())
        fmax = float(self.ui.fmax.text())
        self.vmax = float(self.ui.vmax.text())
        if self.vmax == 0 : self.vmax = None
        self.f_index_min, self.f_index_max = self.get_index_freq(fmin ,fmax)
        self.plot_psd(self.f_index_min, self.f_index_max, self.vmax)

    #=====================================================================
    # Auxiliary function
    #=====================================================================
    def get_index_freq(self, fmin, fmax) :
        """Get the indices of the freq between fmin and fmax"""
        f_index_min, f_index_max = -1, 0
        for freq in self.psd.freqs :
            if freq <= fmin : f_index_min += 1
            if freq <= fmax : f_index_max += 1

        # Just check if f_index_max is not out of bound
        f_index_max = min(len(self.psd.freqs) - 1, f_index_max)
        return f_index_min, f_index_max