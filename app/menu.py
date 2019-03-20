from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from backend.epochs_psd import EpochsPSD
from backend.raw_psd import RawPSD
from app.epochs_psd import EpochsPSDWindow
from app.raw_psd import RawPSDWindow
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

    #=====================================================================
    # Setup functions
    #=====================================================================
    def setup_ui(self) :
        """Setup the ui with initial values and bindings"""
        self.set_boxes()
        self.set_bindings()
        self.init_psd_parameters()
        self.filePath = ''
        self.dataType = None

    #---------------------------------------------------------------------
    def set_bindings(self) :
        """Set all the bindings"""
        self.ui.psdButton.clicked.connect(self.open_psd_visualizer)
        self.ui.pathButton.clicked.connect(self.choose_path)
        self.ui.savePsdButton.clicked.connect(self.choose_save_path)
        self.ui.plotData.clicked.connect(self.plot_data)
        self.ui.psdParametersButton.clicked.connect(self.choose_psd_parameters_path)
        self.ui.lineEdit.editingFinished.connect(self.path_change)
        self.ui.psdParametersLine.editingFinished.connect(self.psd_parameters_path_change)
        self.ui.psdMethod.currentIndexChanged.connect(self.init_psd_parameters)

    #---------------------------------------------------------------------
    def set_boxes(self) :
        """Set the values of the combo boxes"""
        for extension in ['.fif','-epo.fif', '.ep', '.eph', '.sef'] :
            self.ui.chooseFileType.addItem(extension)

        self.ui.psdMethod.addItem('Welch')
        self.ui.psdMethod.addItem('Multitaper')

    #---------------------------------------------------------------------
    def init_psd_parameters(self) :
        """Set the parameters in the parameters text slot"""
        text = "fmin=0\nfmax=40\ntmin=Default\ntmax=Default\n"
        if self.ui.psdMethod.currentText() == 'Welch' :
            text = text + "n_fft=256\nn_per_seg=256\nn_overlap =0"
        if self.ui.psdMethod.currentText() == 'Multitaper' :
            text = text + "bandwidth=4"
        self.ui.psdParametersText.setText(text)

    #=====================================================================
    # Reading data
    #=====================================================================
    def read_data(self) :
        """Set-up the data in mne class"""
        extension = self.ui.chooseFileType.currentText()
        if extension == '.fif' :
            from mne.io import read_raw_fif
            self.dataType = 'raw'
            self.eeg_data = read_raw_fif(self.filePath)

        if extension == '-epo.fif' :
            from mne import read_epochs
            self.dataType = 'epochs'
            self.eeg_data = read_epochs(self.filePath)

        if extension == '.ep' :
            from backend.read import read_ep
            self.dataType = 'raw'
            self.eeg_data = read_ep(self.filePath)

        if extension == '.eph' :
            from backend.read import read_eph
            self.dataType = 'raw'
            self.eeg_data = read_eph(self.filePath)

        if extension == '.sef' :
            from backend.read import read_sef
            self.dataType = 'raw'
            self.eeg_data = read_sef(self.filePath)

    #---------------------------------------------------------------------
    def plot_data(self) :
        """Initialize the data and plot the data on a matplotlib window"""
        try :
            self.read_data()
        except (AttributeError, FileNotFoundError, OSError) :
            self.show_error("Can't find/read file\nPlease verify the path and extension")
        else :
            plt.close('all')
            self.eeg_data.plot(scalings = 'auto')
            plt.show()

    #=====================================================================
    # Open PSD Visualizer
    #=====================================================================
    def open_psd_visualizer(self) :
        """Redirect to PSD Visualize app"""
        try :
            self.read_data()
        except (AttributeError, FileNotFoundError, OSError) :
            self.show_error("Can't find/read file.\nPlease verify the path and extension")
        else :
            self.get_parameters()
            if self.dataType == 'epochs' :
                self.open_epochs_psd_visualizer()
            if self.dataType == 'raw' :
                self.open_raw_psd_visualizer()

    #---------------------------------------------------------------------
    def open_epochs_psd_visualizer(self) :
        """Open PSD visualizer for epochs data"""
        if self.ui.psdMethod.currentText() == 'Welch' :
            n_fft    = int(self.psdParams.get('n_fft', 256))
            self.psd = EpochsPSD(self.eeg_data,
                                 fmin       = self.psdParams['fmin'],
                                 fmax       = self.psdParams['fmax'],
                                 tmin       = self.psdParams['tmin'],
                                 tmax       = self.psdParams['tmax'],
                                 method     = 'welch',
                                 n_fft      = n_fft,
                                 n_per_seg  = int(self.psdParams.get('n_per_seg', n_fft)),
                                 n_overlap  = int(self.psdParams.get('n_overlap', 0)))

        if self.ui.psdMethod.currentText() == 'Multitaper' :
            self.psd = EpochsPSD(self.eeg_data,
                                 fmin       = self.psdParams['fmin'],
                                 fmax       = self.psdParams['fmax'],
                                 tmin       = self.psdParams['tmin'],
                                 tmax       = self.psdParams['tmax'],
                                 method     = 'multitaper',
                                 bandwidth  = int(self.psdParams.get('bandwidth', 4)))

        psdVisualizer = EpochsPSDWindow(self.psd)
        psdVisualizer.show()

    #---------------------------------------------------------------------
    def open_raw_psd_visualizer(self) :
        """Open PSD Visualizer for raw type data"""
        if self.ui.psdMethod.currentText() == 'Welch' :
            n_fft    = int(self.psdParams.get('n_fft', 256))
            self.psd = RawPSD(self.eeg_data,
                              fmin       = self.psdParams['fmin'],
                              fmax       = self.psdParams['fmax'],
                              tmin       = self.psdParams['tmin'],
                              tmax       = self.psdParams['tmax'],
                              method     = 'welch',
                              n_fft      = n_fft,
                              n_per_seg  = int(self.psdParams.get('n_per_seg', n_fft)),
                              n_overlap  = int(self.psdParams.get('n_overlap', 0)))

        if self.ui.psdMethod.currentText() == 'Multitaper' :
            self.psd = RawPSD(self.eeg_data,
                              fmin       = self.psdParams['fmin'],
                              fmax       = self.psdParams['fmax'],
                              tmin       = self.psdParams['tmin'],
                              tmax       = self.psdParams['tmax'],
                              method     = 'multitaper',
                              bandwidth  = int(self.psdParams.get('bandwidth', 4)))

        psdVisualizer = RawPSDWindow(self.psd)
        psdVisualizer.show()

    #=====================================================================
    #Choosing main file path
    #=====================================================================
    def choose_path(self) :
        self.filePath, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "Python Files (*.py)")
        self.ui.lineEdit.setText(self.filePath)

    #---------------------------------------------------------------------
    def path_change(self) :
        self.filePath = self.ui.lineEdit.text()

    #=====================================================================
    #Choosing parameters file path
    #=====================================================================
    def choose_psd_parameters_path(self) :
        self.psdParametersPath, _ = QFileDialog.getOpenFileName(self,"Choose Parameters", "")
        self.ui.psdParametersLine.setText(self.psdParametersPath)
        self.ui.psdParametersText.setText(open(self.psdParametersPath, 'r').read())

    #---------------------------------------------------------------------
    def psd_parameters_path_change(self) :
        self.psdParametersPath = self.ui.psdParametersLine.text()
        self.ui.psdParametersText.setText(open(self.psdParametersPath, 'r').read())

    #=====================================================================
    #Choosing save file path
    #=====================================================================
    def choose_save_path(self) :
        self.savepath = QFileDialog.getSaveFileName(self)

    #=====================================================================
    #Read parameters
    #=====================================================================
    def get_parameters(self) :
        """Get parameters from txt file"""
        # Need to handle all exceptions ...
        text = self.ui.psdParametersText.toPlainText()
        params = text.replace(" ", "").split('\n')
        dic = {}
        for param in params :
            try :
                param, val = param.replace(" ", "").split("=")
            except ValueError :
                print("Format must be of format param_id = value")

            if val == 'Default'or val == 'None' : dic[param] = None
            else : dic[param] = float(val)
        self.psdParams = dic

    #=====================================================================
    #Redirect to epoching window
    #=====================================================================
    def raw_to_epochs(self) :
        """Open the epoching utility window, and get the new epochs"""
        return 0

    #=====================================================================
    # Error handling window
    #=====================================================================
    def show_error(self, msg) :
        error = QMessageBox()
        error.setIcon(QMessageBox.Warning)
        error.setText("Error")
        error.setInformativeText(msg)
        error.setWindowTitle("Error")
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()
