from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from matplotlib.pyplot import close, show
from app.menu_UI import Ui_MenuWindow

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
    # Setup and Initialization functions
    #=====================================================================
    def setup_ui(self) :
        """Setup the ui with initial values and bindings"""
        self.set_boxes()
        self.set_bindings()
        self.init_psd_parameters()
        self.init_tfr_parameters()
        self.filePath = ''
        self.dataType = None

    #---------------------------------------------------------------------
    def set_bindings(self) :
        """Set all the bindings"""
        self.ui.psdButton.clicked.connect(self.open_psd_visualizer)
        self.ui.tfrButton.clicked.connect(self.open_tfr_visualizer)
        self.ui.pathButton.clicked.connect(self.choose_eeg_path)
        self.ui.savePsdButton.clicked.connect(self.choose_save_path)
        self.ui.plotData.clicked.connect(self.plot_data)
        self.ui.displayDataButton.clicked.connect(self.display_data_infos)
        self.ui.psdParametersButton.clicked.connect(self.choose_psd_parameters_path)
        self.ui.lineEdit.editingFinished.connect(self.eeg_path_changed)
        self.ui.psdParametersLine.editingFinished.connect(self.psd_parameters_path_changed)
        self.ui.psdMethod.currentIndexChanged.connect(self.init_psd_parameters)
        self.ui.tfrMethodBox.currentIndexChanged.connect(self.init_tfr_parameters)
        self.ui.epochingButton.clicked.connect(self.open_epoching_window)
        self.ui.electrodeMontage.currentTextChanged.connect(self.choose_xyz_path)

    #---------------------------------------------------------------------
    def set_boxes(self) :
        """Set the values of the combo boxes for file extension, coordinates and fourier methods"""
        for extension in ['.fif','-epo.fif','.sef', '.ep', '.eph'] :
            self.ui.chooseFileType.addItem(extension)

        for method in ['No coordinates', 'Use xyz file', 'standard_1005', 'standard_1020'] :
            self.ui.electrodeMontage.addItem(method)

        self.ui.psdMethod.addItem('multitaper')
        self.ui.psdMethod.addItem('welch')
        self.ui.tfrMethodBox.addItem('multitaper')
        self.ui.tfrMethodBox.addItem('stockwell')
        self.ui.tfrMethodBox.addItem('morlet')

    #---------------------------------------------------------------------
    def init_psd_parameters(self) :
        """Set the parameters in the parameters text slot"""
        text = "fmin=0\nfmax=100\ntmin=Default\ntmax=Default\n"
        if self.ui.psdMethod.currentText() == 'welch' :
            text = text + "n_fft=256\nn_per_seg=256\nn_overlap =0"
        if self.ui.psdMethod.currentText() == 'multitaper' :
            text = text + "bandwidth=4"
        self.ui.psdParametersText.setText(text)

    #---------------------------------------------------------------------
    def init_tfr_parameters(self) :
        """Set the parameters in the parameters text slot"""
        text = "fmin=5\nfmax=100\nfreq_step=1\nn_cycles=3\n"
        if self.ui.tfrMethodBox.currentText() == 'multitaper' :
            text = text + "time_bandwidth=4\n"
        if self.ui.tfrMethodBox.currentText() == 'stockwell' :
            text = text + "width=1\nn_fft=512\n"
        text = text + "picked_channels=0"
        self.ui.tfrParametersText.setText(text)

    #=====================================================================
    # Reading and setting up data
    #=====================================================================
    def read_data(self, tfr = False) :
        """Read all the data entered by the user"""
        self.read_eeg_data()
        self.read_montage()
        self.read_parameters(tfr=tfr)

    #---------------------------------------------------------------------
    def read_eeg_data(self) :
        """Read the eeg data depending on the file"""
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
    def read_montage(self) :
        """Read the montage data"""
        montage = self.ui.electrodeMontage.currentText()
        if montage == 'Use xyz file' :
            from backend.util import xyz_to_montage
            montage = xyz_to_montage(self.ui.xyzPath.text())
            self.eeg_data.set_montage(montage)
        elif montage != 'No coordinates' :
            from mne.channels import read_montage
            self.eeg_data.set_montage(read_montage(montage))

    #---------------------------------------------------------------------
    def read_parameters(self, tfr = False) :
        """Read parameters from txt file and sets it up in params"""
        if tfr :
            text = self.ui.tfrParametersText.toPlainText()
        else :
            text = self.ui.psdParametersText.toPlainText()
        params = text.replace(" ", "").split('\n')
        dic = {}
        try :
            for param in params :
                param, val = param.replace(" ", "").split("=")
                if val == 'Default'or val == 'None' : dic[param] = None
                else :
                    val = val.split(",")
                    if len(val) == 1 :
                        dic[param] = float(val[0])
                    else :
                        dic[param] = [float(e) for e in val]

        except ValueError :
                self.show_error("Format of parameters must be param_id = values")
        self.params = dic

    #---------------------------------------------------------------------
    def plot_data(self) :
        """Initialize the data and plot the data on a matplotlib window"""
        try :
            self.read_data()
        except (AttributeError, FileNotFoundError, OSError) :
            self.show_error("Can't find/read file\nPlease verify the path and extension")
        except (ValueError) :
            self.show_error("Names of electrodes don't fit convention")
        else :
            close('all')
            self.eeg_data.plot(scalings = 'auto')
            show()

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
            if self.dataType == 'epochs' :
                self.open_epochs_psd_visualizer()
            if self.dataType == 'raw' :
                self.open_raw_psd_visualizer()

    #---------------------------------------------------------------------
    def init_epochs_psd(self) :
        """Initialize the instance of EpochsPSD"""
        from backend.epochs_psd import EpochsPSD

        if self.ui.psdMethod.currentText() == 'welch' :
            n_fft    = int(self.params.get('n_fft', 256))
            self.psd = EpochsPSD(self.eeg_data,
                                 fmin       = self.params['fmin'],
                                 fmax       = self.params['fmax'],
                                 tmin       = self.params['tmin'],
                                 tmax       = self.params['tmax'],
                                 method     = 'welch',
                                 n_fft      = n_fft,
                                 n_per_seg  = int(self.params.get('n_per_seg', n_fft)),
                                 n_overlap  = int(self.params.get('n_overlap', 0)))

        if self.ui.psdMethod.currentText() == 'multitaper' :
            self.psd = EpochsPSD(self.eeg_data,
                                 fmin       = self.params['fmin'],
                                 fmax       = self.params['fmax'],
                                 tmin       = self.params['tmin'],
                                 tmax       = self.params['tmax'],
                                 method     = 'multitaper',
                                 bandwidth  = int(self.params.get('bandwidth', 4)))

    #---------------------------------------------------------------------
    def init_raw_psd(self) :
        """Initialize the instance of RawPSD"""
        from backend.raw_psd import RawPSD

        if self.ui.psdMethod.currentText() == 'welch' :
            n_fft    = int(self.params.get('n_fft', 256))
            self.psd = RawPSD(self.eeg_data,
                              fmin       = self.params['fmin'],
                              fmax       = self.params['fmax'],
                              tmin       = self.params['tmin'],
                              tmax       = self.params['tmax'],
                              method     = 'welch',
                              n_fft      = n_fft,
                              n_per_seg  = int(self.params.get('n_per_seg', n_fft)),
                              n_overlap  = int(self.params.get('n_overlap', 0)))

        if self.ui.psdMethod.currentText() == 'multitaper' :
            self.psd = RawPSD(self.eeg_data,
                              fmin       = self.params['fmin'],
                              fmax       = self.params['fmax'],
                              tmin       = self.params['tmin'],
                              tmax       = self.params['tmax'],
                              method     = 'multitaper',
                              bandwidth  = int(self.params.get('bandwidth', 4)))

    #---------------------------------------------------------------------
    def open_epochs_psd_visualizer(self) :
        """Open PSD visualizer for epochs data"""
        from app.epochs_psd import EpochsPSDWindow

        self.init_epochs_psd()
        psdVisualizer = EpochsPSDWindow(self.psd)
        psdVisualizer.show()

    #---------------------------------------------------------------------
    def open_raw_psd_visualizer(self) :
        """Open PSD Visualizer for raw type data"""
        from app.raw_psd import RawPSDWindow

        self.init_raw_psd()
        psdVisualizer = RawPSDWindow(self.psd)
        psdVisualizer.show()

    #=====================================================================
    # Open epoching window
    #=====================================================================
    def open_epoching_window(self) :
        from app.epoching import EpochingWindow

        window = EpochingWindow()
        window.ui.rawLine.setText(self.filePath)
        window.exec_()

    #=====================================================================
    # Open TFR Window
    #=====================================================================
    def init_pick_tfr(self) :
        """Init list with picks"""
        picks = self.params['picked_channels']
        if type(picks) == list :
            return [int(ch) for ch in picks]
        else :
            return [int(picks)]

    def init_avg_tfr(self) :
        """Init tfr from parameters"""
        from backend.avg_epochs_tfr import AvgEpochsTFR
        from numpy import arange

        freqs = arange(self.params['fmin'], self.params['fmax'], self.params['freq_step'])
        n_cycles = self.params['n_cycles']
        picks = self.init_pick_tfr()
        self.avgTFR = AvgEpochsTFR(self.eeg_data, freqs, n_cycles,
                                   method         = self.ui.psdMethod.currentText(),
                                   time_bandwidth = self.params.get('time_bandwidth', None),
                                   n_fft          = self.params.get('n_fft', None),
                                   width          = self.params.get('width', None),
                                   picks          = picks)

    def open_tfr_visualizer(self) :
        """Open TFR Visualizer for epochs"""
        from app.avg_epochs_tfr import AvgTFRWindow

        try :
            self.read_data(tfr=True)
        except (AttributeError, FileNotFoundError, OSError) :
            self.show_error("Can't find/read file.\nPlease verify the path and extension")
        else :
            self.init_avg_tfr()
            psdVisualizer = AvgTFRWindow(self.avgTFR)
            psdVisualizer.show()

    #=====================================================================
    #Choosing different path
    #=====================================================================
    def choose_eeg_path(self) :
        """Open window for choosing eeg path and updates the line"""
        self.filePath, _ = QFileDialog.getOpenFileName(self,"Choose data path", "Python Files (*.py)")
        self.ui.lineEdit.setText(self.filePath)

    #---------------------------------------------------------------------
    def eeg_path_changed(self) :
        """Gets called when eeg path is changed"""
        self.filePath = self.ui.lineEdit.text()

    #---------------------------------------------------------------------
    def choose_psd_parameters_path(self) :
        """Open window for choosing PSD parameters path"""
        self.psdParametersPath, _ = QFileDialog.getOpenFileName(self,"Choose Parameters", "")
        self.ui.psdParametersLine.setText(self.psdParametersPath)
        self.ui.psdParametersText.setText(open(self.psdParametersPath, 'r').read())

    #---------------------------------------------------------------------
    def psd_parameters_path_changed(self) :
        """Gets called when PSD parameters are changed"""
        self.psdParametersPath = self.ui.psdParametersLine.text()
        self.ui.psdParametersText.setText(open(self.psdParametersPath, 'r').read())

    #---------------------------------------------------------------------
    def choose_xyz_path(self) :
        """Gets called when electrode montage box is updated"""
        if self.ui.electrodeMontage.currentText() == 'Use xyz file' :
            self.xyzPath, _ = QFileDialog.getOpenFileName(self,"Choose .xyz file", "")
            self.ui.xyzPath.setText(self.xyzPath)

    #=====================================================================
    #Choosing save file path
    #=====================================================================
    def choose_save_path(self) :
        """Open window for choosing save path"""
        self.savepath, _ = QFileDialog.getSaveFileName(self)
        try :
            self.read_data()
        except (AttributeError, FileNotFoundError, OSError) :
            self.show_error("Can't find/read file.\nPlease verify the path and extension")
        else :
            if self.dataType == 'epochs' : self.init_epochs_psd()
            if self.dataType == 'raw'    : self.init_raw_psd()
            self.save_matrix_txt()

    #---------------------------------------------------------------------
    def save_matrix_txt(self) :
        """Save the matrix containing the PSD"""
        self.psd.save_matrix_txt(self.savepath)

    #=====================================================================
    # Display data informations
    #=====================================================================
    def display_data_infos(self) :
        """Display informations about data on a pop-up window"""
        try :
            self.read_data()
        except (AttributeError, FileNotFoundError, OSError) :
            self.show_error("Can't find/read file\nPlease verify the path and extension")
        else :
            self.show_infos(self.init_info_string())

    #---------------------------------------------------------------------
    def init_info_string(self) :
        """Init a string with informations about data"""
        infos = "Sampling Frequency : {}\nNumber of Channels : {}\n".format(
                self.eeg_data.info["sfreq"], self.eeg_data.info["nchan"])
        if self.dataType == 'raw' :
            infos = infos + "Number of Time points : {}".format(self.eeg_data.n_times)
        if self.dataType == 'epochs' :
            infos = infos + "Number of Time points per Epoch : {}".format(len(self.eeg_data.times))
        return infos

    #=====================================================================
    # Pop up windows for error and informations
    #=====================================================================
    def show_error(self, msg) :
        """Display window with an error message"""
        error = QMessageBox()
        error.setBaseSize(QSize(800, 200))
        error.setIcon(QMessageBox.Warning)
        error.setText("Error")
        error.setInformativeText(msg)
        error.setWindowTitle("Error")
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()

    #---------------------------------------------------------------------
    def show_infos(self, msg) :
        """Display a window with an information message"""
        info = QMessageBox()
        info.setBaseSize(QSize(800, 200))
        info.setIcon(QMessageBox.Information)
        info.setText("Data informations")
        info.setInformativeText(msg)
        info.setWindowTitle("Data Informations")
        info.exec_()
