from mne.io import read_raw_fif
from backend.raw_psd import RawPSD


fmin = 5
fmax = 100
raw = read_raw_fif('brainHackTestClosed_processed-raw.fif')
