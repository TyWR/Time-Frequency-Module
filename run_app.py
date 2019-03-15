from PyQt5.QtWidgets import QDialog, QApplication
import sys
import os
os.chdir('/home/tvivier/Python/Time-Frequency-Module')

from app.psd import PSDWindow
from app.data import ImportDataWindow
from backend.psd import EpochsPSD
from data.example_1 import get_example1

epochs = get_example1()
epochsPSD = EpochsPSD(epochs, fmin = 0, fmax = 40, tmin = 0, tmax = 0.5, method = 'welch', n_fft = 2048, n_per_seg = 30, n_overlap = 15)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = PSDWindow(epochsPSD)
    main.show()
    sys.exit(app.exec_())
