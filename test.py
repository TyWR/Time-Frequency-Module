import mne
from mne import io
from mne.datasets import sample
from processing import EpochsPSD
import matplotlib.pyplot as plt
%matplotlib qt
print(__doc__)

data_path = sample.data_path()

raw_fname = data_path + '/MEG/sample/sample_audvis_filt-0-40_raw.fif'
event_fname = data_path + '/MEG/sample/sample_audvis_filt-0-40_raw-eve.fif'
event_id, tmin, tmax = 1, -0.2, 0.5

# Setup for reading the raw data
raw = io.read_raw_fif(raw_fname)
events = mne.read_events(event_fname)

# Set up pick list: EEG + MEG - bad channels (modify to your needs)
raw.info['bads'] += ['MEG 2443', 'EEG 053']  # bads + 2 more
picks = mne.pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False,
                       exclude='bads')

# Read epochs
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, proj=True,
                    picks=picks, baseline=(None, 0), preload=True)


# Compute all the psds
psd = EpochsPSD(epochs, fmin = 0, fmax = 100, tmin = 0, tmax = 0.5, method = 'welch', n_fft = 256, n_per_seg = 30, n_overlap = 15)

# Choose a frequency in the list
freq_index = 17             # for f = 9.97114 Hz
psd.plot_map_epoch(3, 17)   # Plot power for 3rd epoch, and f = 9.97114 Hz
