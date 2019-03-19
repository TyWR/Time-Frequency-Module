import mne
from mne import io
from mne.datasets import sample
from backend.raw_psd import RawPSD
import matplotlib.pyplot as plt
from app.raw_psd import RawPSDWindow
from PyQt5.QtWidgets import QDialog, QApplication
import sys

print(__doc__)

data_path = sample.data_path()
raw_fname = data_path + '/MEG/sample/sample_audvis_filt-0-40_raw.fif'
event_fname = data_path + '/MEG/sample/sample_audvis_filt-0-40_raw-eve.fif'
event_id, tmin, tmax = 1, -0.2, 0.5

# Setup for reading the raw data
raw = io.read_raw_fif(raw_fname, preload = True)

raw = raw.pick_types(meg=False, eeg=True, eog=False,
                       stim=False, exclude='bads')

rawPSD = RawPSD(raw, 0, 40, tmax = 20, method = 'welch')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = RawPSDWindow(rawPSD)
    main.show()
    sys.exit(app.exec_())
