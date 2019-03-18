from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os
from backend.psd import EpochsPSD
from app.psd import PSDWindow
from app.menu_UI import Ui_MenuWindow
import matplotlib.pyplot as plt
import _thread
"""
File containing the main window class, ie the window for selectionning
the path of the dataset, choose the parameters for computing the PSD etc.
"""
class MenuWindow(QMainWindow) :

    def __init__(self) :
        super(MenuWindow, self).__init__(parent = None)
        self.setWindowTitle("Open PSD Visualize")
        self.ui = Ui_MenuWindow()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.setup_ui()

    #---------------------------------------------------------------------
    def setup_ui(self) :
        """Setup the ui with initial values and bindings"""
        self.set_sliders()
        self.set_bindings()
        self.init_psd_parameters()

    #---------------------------------------------------------------------
    def set_bindings(self) :
        """Set all the bindings"""
        self.ui.psdButton.clicked.connect(self.open_psd_visualizer)
        self.ui.pathButton.clicked.connect(self.choose_path)
        self.ui.lineEdit.editingFinished.connect(self.path_change)
        self.ui.plotData.clicked.connect(self.plot_data)
        self.ui.psdMethod.currentIndexChanged.connect(self.init_psd_parameters)

    #---------------------------------------------------------------------
    def set_sliders(self) :
        """Set slider for extensions"""
        for extension in ['.fif','.ep', '.eph', '.sef'] :
            self.ui.chooseFileType.addItem(extension)

        self.ui.psdMethod.addItem('Welch')
        self.ui.psdMethod.addItem('Multitaper')

    #---------------------------------------------------------------------
    def init_psd_parameters(self) :
        """Set the parameters in the parameters text slot"""
        if self.ui.psdMethod.currentText() == 'Welch' :
            self.ui.psdParameters.setText("fmin=0\nfmax=40\ntmin=Default\ntmax=Default\n"+
                                            "n_fft=256\nn_per_seg=256\nn_overlap =0")
        if self.ui.psdMethod.currentText() == 'Multitaper' :
            self.ui.psdParameters.setText("fmin=0\nfmax=40\ntmin=Default\ntmax=Default\n"+
                                          "bandwidth=4")

    #---------------------------------------------------------------------
    def get_parameters(self) :
        """Get parameters from txt file"""
        # Need to handle all exceptions ...
        text = self.ui.psdParameters.toPlainText()
        params = text.replace(" ", "").split('\n')
        dic = {}
        for param in params :
            param, val = param.replace(" ", "").split("=")
            if val == 'Default'or val == 'None':
                dic[param] = None
            else :
                dic[param] = float(val)
        self.psdParams = dic

    #---------------------------------------------------------------------
    def read_data(self) :
        """Set-up the data in mne class"""
        extension = self.ui.chooseFileType.currentText()
        if extension == '.fif' :
            from mne import read_epochs
            self.epochs = read_epochs(self.filePath)

    #---------------------------------------------------------------------
    def plot_data(self) :
        """Initialize the data and plot the data on a new thread"""
        def run() :
            plt.close('all')
            self.epochs.plot()
            plt.show()

        self.read_data()
        _thread.start_new_thread(run, ())

    #---------------------------------------------------------------------
    def open_psd_visualizer(self) :
        """Redirect to PSD Visualize app"""
        self.read_data()
        self.get_parameters()
        print(self.psdParams)
        if self.ui.psdMethod.currentText() == 'Welch' :
            self.psd = EpochsPSD(self.epochs,
                                 fmin       = self.psdParams['fmin'],
                                 fmax       = self.psdParams['fmax'],
                                 tmin       = self.psdParams['tmin'],
                                 tmax       = self.psdParams['tmax'],
                                 method     = 'welch',
                                 n_fft      = int(self.psdParams['n_fft']),
                                 n_per_seg  = int(self.psdParams['n_per_seg']),
                                 n_overlap  = int(self.psdParams['n_overlap']))

        if self.ui.psdMethod.currentText() == 'Multitaper' :
            self.psd = EpochsPSD(self.epochs,
                                 fmin       = self.psdParams['fmin'],
                                 fmax       = self.psdParams['fmax'],
                                 tmin       = self.psdParams['tmin'],
                                 tmax       = self.psdParams['tmax'],
                                 method     = 'multitaper',
                                 bandwidth  = int(self.psdParams['bandwidth']))

        psdVisualizer = PSDWindow(self.psd)
        psdVisualizer.show()

    #=====================================================================
    # Choosing path
    def choose_path(self) :
        self.filePath, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "Python Files (*.py)")
        self.ui.lineEdit.setText(self.filePath)

    #---------------------------------------------------------------------
    def path_change(self) :
        self.filePath = self.ui.lineEdit.text()
