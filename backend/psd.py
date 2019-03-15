"""
=================================================================================
                                    psd

This file contains several functions to compute PSD on epochs. It creates a instance
of a class called EpochsDSP. EpochsDSP enable to handle all the psds data from all the
different epochs. This class also comes with different methods to visualize the psds.
=================================================================================
"""
from mne.time_frequency import psd_multitaper, psd_welch
from mne.viz import plot_topomap
import matplotlib.pyplot as plt
from numpy import mean


class EpochsPSD :
    """
    This class contains the PSD of a set of Epochs. It stores the data of the psds of
    each epoch. The psds are calculated with the Library mne.

    Attributes :
    ============
    fmin        (float)         : frequency limit
    fmax        (float)         : frequency limit
    tmin        (float)         : lower time bound for each epoch
    tmax        (float)         : higher time bound for each epoch
    info        (mne Infos)     : info of the epochs
    method      (str)           : method used for PSD (multitaper or welch)
    data        (numpy arr.)    : dataset with all the psds data (n_epochs, n_channels, n_freqs)
    freqs       (arr.)          : list containing the frequencies of the psds

    Methods :
    ============
    __init__                    : Compute all the PSD of each epoch
    plot_topomap                : Plot the map of the power for a given frequency and epoch
    plot_topomap_band           : Plot the map of the power for a given band frequency and epoch
    plot_avg_topomap_band       : Plot the map of the power for a given band, averaged over epochs
    """

    def __init__(self, epochs, fmin = 0, fmax = 1500, tmin = None, tmax = None, method = 'multitaper', **kwargs) :
        """
        Computes the PSD of the epochs with the correct method multitaper or welch.

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

        self.bandwidth = kwargs.get('bandwidth', 4.)
        self.n_fft     = kwargs.get('n_fft', 256)
        self.n_per_seg = kwargs.get('n_per_seg', self.n_fft)
        self.n_overlap = kwargs.get('n_overlap', 0)


        if method == 'multitaper' :
            print("Computing Mulitaper PSD with parameter bandwidth = {} on {} Epochs".format(
                  self.bandwidth, len(self.info['chs'])))
            self.data, self.freqs = psd_multitaper(epochs,
                                                   fmin             = fmin,
                                                   fmax             = fmax,
                                                   tmin             = tmin,
                                                   tmax             = tmax,
                                                   normalization    = 'full',
                                                   bandwidth        = self.bandwidth)

        if method == 'welch'      :
            print("Computing Welch PSD with parameters n_fft = {}, n_per_seg = {}, n_overlap = {} on {} Epochs".format(
                  self.n_fft, self.n_per_seg, self.n_overlap, len(self.info['chs'])))
            self.data, self.freqs = psd_welch(epochs,
                                              fmin      = fmin,
                                              fmax      = fmax,
                                              tmin      = tmin,
                                              tmax      = tmax,
                                              n_fft     = self.n_fft,
                                              n_overlap = self.n_overlap,
                                              n_per_seg = self.n_per_seg)

    def __str__(self) :
        string = "PSD Computed on {} Epochs with method {}.\nParameters : \n".format(len(self.info['chs']), self.method)
        string = string + "fmin : {}Hz, fmax : {}Hz (with {} frequency points)\n".format(self.fmin, self.fmax, len(self.freqs))
        string = string + "tmin : {}s, tmax : {}s\n".format(self.tmin, self.tmax)
        if self.method == 'welch' :
            string = string + "n_fft : {}, n_per_seg : {}, n_overlap : {}\n".format(
                self.n_fft, self.n_per_seg, self.n_overlap)
        else :
            string = string + "bandwidth : {}".format(self.bandwidth)
        return string

    def plot_topomap(self, epoch_index, freq_index, axes = None) :
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
        Instance of Matplotlib.Image
        """
        # Handling error if no coordinates are found
        if self.info['chs'][0]['loc'] is None :
            raise ValueError("No locations available for this dataset")

        psd_values = self.data[epoch_index, :, freq_index]
        return plot_topomap(psd_values, self.info, axes = axes, show = False, cmap = 'GnBu')

    def plot_topomap_band(self, epoch_index, freq_index_min, freq_index_max, axes = None, vmin = None, vmax = None) :
        """
        Plot the map of the power for a given frequency band chosen by freq_index_min and freq_index_max
        , the frequency is hence the value self.freqs[freq_index]. This function will return an error if
        the class is not initialized with the coordinates of the different electrodes.

        Arguments :
        ============
        epoch_index    (int)        : index of the epoch in epochs
        freq_index_max (int)        : index of the min frequency in self.freqs
        freq_index_min (int)        : index of the max frequency in self.freqs
        axes
        vmin
        vmax

        Returns :
        ============
        Instance of Matplotlib.Image
        """
        # Handling error if no coordinates are found
        if self.info['chs'][0]['loc'] is None :
            raise ValueError("No locations available for this dataset")

        psd_values = self.data[epoch_index, :, freq_index_min : freq_index_max]
        psd_mean = mean(psd_values, axis = 1)
        return plot_topomap(psd_mean, self.info, axes = axes, vmin = vmin, vmax = vmax, show = False, cmap = 'GnBu')

    def plot_avg_topomap_band(self, freq_index_min, freq_index_max, axes = None, vmin = None, vmax = None) :
        """
        Plot the map of the average power for a given frequency band chosen by freq_index_min and
        freq_index_max, the frequency is hence the value self.freqs[freq_index]. This function will
        return an error if the class is not initialized with the coordinates of the different
        electrodes.

        Arguments :
        ============
        freq_index_max (int)        : index of the min frequency in self.freqs
        freq_index_min (int)        : index of the max frequency in self.freqs


        Returns :
        ============
        Instance of Matplotlib.Image
        """
        # Handling error if no coordinates are found
        if self.info['chs'][0]['loc'] is None :
            raise ValueError("No locations available for this dataset")

        psd_values = self.data[:, :, freq_index_min : freq_index_max]
        psd_mean = mean(psd_values, axis = 2)  #average over frequency band
        psd_mean = mean(psd_mean,   axis = 0)  #average over epochs
        return plot_topomap(psd_mean, self.info, axes = axes, vmin = vmin, vmax = vmax, show = False, cmap = 'GnBu')

    def plot_psd_matrix(self, freq_index_min, freq_index_max, axes = None, vmin = None, vmax = None) :
        """
        Plot the map of the average power for a given frequency band chosen by freq_index_min and
        freq_index_max, the frequency is hence the value self.freqs[freq_index]. This function will
        return an error if the class is not initialized with the coordinates of the different
        electrodes.

        Arguments :
        ============
        freq_index_max (int)        : index of the min frequency in self.freqs
        freq_index_min (int)        : index of the max frequency in self.freqs
        axes
        vmin
        vmax


        Returns :
        ============
        Instance of Matplotlib.Image
        """
        extent = [self.freqs[freq_index_min], self.freqs[freq_index_max], 1, self.info['nchan']]
        mat = mean(self.data[:, :, freq_index_min : freq_index_max], axis = 0)
        return plt.matshow(mat, extent = extent, cmap = 'GnBu')
