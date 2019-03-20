# -*- coding: utf-8 -*-
from backend.read import read_sef
import matplotlib.pyplot as plt
%matplotlib qt
import mne
import numpy as np
from backend.raw_psd import RawPSD
import struct
import codecs



raw = read_sef('data/EEG_cdt2.Export.sef')
raw.info
montage = mne.channels.read_montage('standard_1005')
raw.set_montage(montage)
raw.info['ch_names']
psd = RawPSD(raw, tmin = 0, tmax = 2)
psd.plot_topomap(1)





f = open('data/EEG_cdt1.Export.sef', 'rb')
#   Read fixed part of the header
version             = f.read(4).decode('utf-8')
n_channels,         = struct.unpack('I', f.read(4))
num_aux_electrodes, = struct.unpack('I', f.read(4))
num_time_frames,    = struct.unpack('I', f.read(4))
sfreq,              = struct.unpack('f', f.read(4))
year,               = struct.unpack('H', f.read(2))
month,              = struct.unpack('H', f.read(2))
day,                = struct.unpack('H', f.read(2))
hour,               = struct.unpack('H', f.read(2))
minute,             = struct.unpack('H', f.read(2))
second,             = struct.unpack('H', f.read(2))
millisecond,        = struct.unpack('H', f.read(2))
string = f.read(8)
string
decoded = struct.unpack('', string)
print(decoded)

for k in range(n_channels) :
    ch_names.append(f.read(8).decode('utf-8'))
