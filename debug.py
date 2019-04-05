from backend.raw_psd import RawPSD
from mne.io import read_raw_fif
from mne.channels import read_montage



raw = read_raw_fif('brainHackTestClosed-raw.fif')
montage = read_montage('standard_1020')
raw.set_montage(montage)
psd = RawPSD(raw, fmin = 5, fmax = 20, tmin = 20, tmax = 25, montage = montage)
psd.plot_topomap(1)
