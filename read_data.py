"""
Module contenant les fonctions suivantes, destinées à lire pour MNE différents types de fichier :

A tester sur plusieurs fichier ...

"""
from mne.io import RawArray
from mne import create_info
import numpy as np
import struct

def read_ep(path, **kwargs) :
    """
    =================================================================================
    *
    *   read file with format .ep, and returns a mne.io.Raw object containing
    *   the data.
    *   ***********************************************************************************
    *   path (str)                      : datapath of the .ep file
    *   ch_names (array(str))           : names of the channels (default EEG(number))
    *   sfreq (float)                   : sampling frequency
    *  ***********************************************************************************
    *   output :
    *   mne.io.Raw
    =================================================================================
    """
    data = np.loadtxt(path, unpack = True)
    n_channels = data.shape[0]

    ch_names = ['EEG{}'.format(i) for i in range(n_channels)]
    sfreq = 1e3
    ch_types = ['eeg' for i in range(n_channels)]
    if kwargs is not None :
        for key, value in kwargs.items() :
            # ch_name argument
            if key == 'ch_names' :
                if len(value) != n_channels :
                    raise ValueError("length of ch_names is {} whereas n_channel = {}".format(len(value), n_channels))
                ch_names = value
            # sfreq argument
            elif key == 'sfreq' : sfreq = value
            # keyword error
            else : raise ValueError("Incorrect keyword, must be ch_names or sfreq")

    infos = create_info(ch_names = ch_names, sfreq = sfreq, ch_types = ch_types)
    return RawArray(data, infos)

def read_eph(path, **kwargs) :
    """
    =================================================================================
    *                                   read_eph
    *
    *   read file with format .eph, and returns a mne.io.Raw object containing
    *   the data.
    *   ***********************************************************************************
    *   input :
    *   path (str)                      : datapath of the .eph file
    *   ch_names (array[str])           : names of the channels (default EEG(number))
    *   ***********************************************************************************
    *   output                          : mne.io.Raw
    =================================================================================
    """
    # Read parameters from header and data
    with open(path, 'r') as file:
        n_channels, n_times, sfreq = file.readline().strip('\n').split(' ')
        n_channels, n_times        = int(n_channels), int(n_times)
    data = np.genfromtxt(path, skip_header = 1, unpack = True)

    ch_names = ['EEG{}'.format(i + 1) for i in range(n_channels)]
    ch_types = ['eeg' for i in range(n_channels)]
    if kwargs is not None :
        for key, value in kwargs.items() :
            # ch_name argument
            if key == 'ch_names' :
                if len(value) != n_channels :
                    raise ValueError("length of ch_names is {} whereas n_channel = {}".format(len(value), n_channels))
                ch_names = value
            # keyword error
            else : raise ValueError("Incorrect keyword must be ch_names")

    infos = create_info(ch_names = ch_names, sfreq = sfreq, ch_types = ch_types)
    return RawArray(data, infos)

def read_sef(path) :
    """
    =================================================================================
    *                                   read_sef
    *
    *   read file with format .eph, and returns a mne.io.Raw object containing
    *   the data.
    *   ***********************************************************************************
    *   input :
    *   path (str)                      : datapath of the .sef file
    *   ch_names (array[str])           : names of the channels (default EEG(number))
    *   ***********************************************************************************
    *   output                          : mne.io.Raw
    =================================================================================
    """
    f = open(path, 'rb')
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

    #   Read variable part of the header
    ch_names = []
    for k in range(n_channels) :
        ch_names.append(f.read(8).decode('utf-8').rstrip('\x00'))

    # Read data
    buffer = np.frombuffer(f.read(n_channels * num_time_frames * 8), dtype=np.float32)
    data = np.reshape(buffer, (n_channels, num_time_frames))

    ch_types = ['eeg' for i in range(n_channels)]
    infos = create_info(ch_names = ch_names, sfreq = sfreq, ch_types = ch_types)
    return RawArray(data, infos)
