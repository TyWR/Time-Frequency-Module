"""
=================================================================================
                                Processing

This file contains several functions to compute PSD on epochs. It creates a instance
of a class called EpochsDSP. This class will contain all the DSPs informations of a
set of epochs.
=================================================================================
"""
from mne.time_frequency import psd_multitaper, psd_welch
from mne.viz import plot_topomap
import matplotlib.pyplot as plt
from numpy import mean


class EpochsPSD :
    """
    This class contains the PSD of a set of Epochs.

    Attributes :
    ============
    fmin        (float)         : frequency limit
    fmax        (float)         : frequency limit
    tmin        (float)         : lower time bound for each epoch
    tmax        (float)         : higher time bound for each epoch
    info        (mne Infos)     : info of the epochs
    method      (str)           : method used for PSD (multitaper or welch)

    Methods :
    ============
    __init__                    : Compute all the PSD of each epoch
    plot_topomap_frequency      : Plot the map of the power for a given frequency and epoch
    plot_topomap_band_frequency : Plot the map of the power for a given band frequency and epoch
    """


    def __init__(self, epochs, fmin = 0, fmax = 1500, tmin = None, tmax = None, method = 'multitaper', **kwargs) :
        """
        Computes the PSD of the epochs with the correct method multitaper or welch

        Arguments :
        ============
        epochs (mne Epochs)         : Instance of epochs to be processed
        method (str)                : 'multitaper' or 'welch'
        n_fft (int)                 : welch parameter for n_fft                 (default = 256)
        n_per_seg (int)             : welch parameter for number of segments    (default = n_fft)
        n_overlap (int)             : welch parameter for overlaping            (default = 0)
        bandwidth (float)           : multitaper parameter for bandwidth        (default = 4.)

        Returns :
        ============
        None
        """
        self.fmin, self.fmax = fmin, fmax
        self.tmin, self.tmax = tmin, tmax

        self.info            = epochs.info
        self.method          = method

        if method == 'multitaper' :
            bandwidth = kwargs.get('bandwidth', 4.)

            print("Computing Mulitaper PSD with parameter bandwidth = {} on {} Epochs ...".format(
                  bandwidth, len(self.info['chs'])))
            self.data, self.freqs = psd_multitaper(epochs, fmin = fmin, fmax = fmax, tmin = tmin, tmax = tmax, bandwidth = bandwidth)


        if method == 'welch'      :
            n_fft     = kwargs.get('n_fft', 256)
            n_per_seg = kwargs.get('n_per_seg', n_fft)
            n_overlap = kwargs.get('n_overlap', 0)

            print("Computing Welch PSD with parameters n_fft = {}, n_per_seg = {}, n_overlap = {} on {} Epochs ...".format(
                  n_fft, n_per_seg, n_overlap, len(self.info['chs'])))
            self.data, self.freqs = psd_welch(epochs, fmin = fmin, fmax = fmax,
                                              tmin = tmin, tmax = tmax,
                                              n_fft = n_fft,
                                              n_overlap = n_overlap,
                                              n_per_seg = n_per_seg)

    def plot_topomap_frequency(self, epoch_index, freq_index, axes = None) :
        """
        Plot the map of the power for a given frequency chosen by freq_index, the frequency
        is hence the value self.freqs[freq_index]. This function will return an error if the class
        is not initialized with the coordinates of the different electrodes.

        Arguments :
        ============
        epoch_index (int)           : index of the epoch in epochs
        freq_index  (int)           : index of the frequency in self.freqs

        Returns :
        ============
        None
        """
        # Handling error if no coordinates are found
        if self.info['chs'][0]['loc'] is None :
            raise ValueError("No locations available for this dataset")

        psd_values = self.data[epoch_index, :, freq_index]
        plot_topomap(psd_values, self.info, axes = axes)


    def plot_topomap_band_frequency(self, epoch_index, freq_index_min, freq_index_max, axes = None) :
        """
        Plot the map of the power for a given frequency band chosen by freq_index_min and freq_index_max
        , the frequency is hence the value self.freqs[freq_index]. This function will return an error if
        the class is not initialized with the coordinates of the different electrodes.

        Arguments :
        ============
        epoch_index    (int)        : index of the epoch in epochs
        freq_index_max (int)        : index of the min frequency in self.freqs
        freq_index_min (int)        : index of the max frequency in self.freqs


        Returns :
        ============
        None
        """
        # Handling error if no coordinates are found
        if self.info['chs'][0]['loc'] is None :
            raise ValueError("No locations available for this dataset")

        psd_values = self.data[epoch_index, :, freq_index_min : freq_index_max]
        print(psd_values.shape)
        psd_mean = mean(psd_values, axis = 1)
        plot_topomap(psd_mean, self.info, axes = axes)
