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


class EpochsPSD :
    """
    Class enable to handle data returned from a function that computes PSD from
    Epochs
    """
    def __init__(self, epochs, fmin = 0, fmax = 1500, tmin = None, tmax = None, method = 'multitaper', **kwargs) :
        """
        =================================================================================
        *
        *   Computes the PSD of the epochs with the correct method multitaper or welch
        *   ***********************************************************************************
        *   input :
        *   epochs          : Instance of epochs
        *   method          : 'multitaper' or 'welch'
        *   n_fft           : welch parameter for n_fft                 (default = 256)
        *   n_per_seg       : welch parameter for number of segments    (default = 3.)
        *   n_overlap       : welch parameter for overlaping            (default = 0)
        *   bandwidth       : multitaper parameter for bandwidth        (default = 4.)
        *   ***********************************************************************************
        *   output :
        *   instance of EpochsPSD
        =================================================================================
        """
        self.fmin, self.fmax = fmin, fmax
        self.tmin, self.tmax = tmin, tmax

        self.ch_names        = epochs.ch_names
        self.info            = epochs.info
        self.method          = method

        if method == 'multitaper' :
            bandwidth = kwargs.get('bandwidth', 4.)
            self.psds, self.freqs = psd_multitaper(epochs, fmin = fmin, fmax = fmax, tmin = tmin, tmax = tmax, bandwidth = bandwidth)

        if method == 'welch'      :
            n_fft     = kwargs.get('n_fft', 256)
            n_per_seg = kwargs.get('n_per_seg', n_fft)
            n_overlap = kwargs.get('n_overlap', 0)
            self.psds, self.freqs = psd_welch(epochs, fmin = fmin, fmax = fmax,
                                              tmin = tmin, tmax = tmax,
                                              n_fft = n_fft,
                                              n_overlap = n_overlap,
                                              n_per_seg = n_per_seg)




    def get_psd_epoch(self, epoch_index) :
        """
        =================================================================================
        *   Get all the psds of the epoch of rank epoch_index
        *   ***********************************************************************************
        *   output :
        *   psds (numpy array)  : array of shape (n_channels, n_freqs)
        =================================================================================
        """
        return self.psds[epoch_index, :, :]




    def plot_map_epoch(self, epoch_index, freq_index, axes = None) :
        """
        =================================================================================
        *   Plot the powers of an epoch for a given frequency
        =================================================================================
        """
        psd_values = self.psds[epoch_index, :, freq_index]
        plot_topomap(psd_values, self.info, axes = axes)
        plt.title("Map of Power for the frequency {}".format(self.freqs[freq_index]))
