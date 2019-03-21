"""
=================================================================================
                                    psd

This file contains several functions to compute PSD on raw file. It creates a instance
of a class called EpochsDSP. EpochsDSP enable to handle all the psds data from all the
different epochs. This class also comes with different methods to visualize the psds.
=================================================================================
"""
from mne.time_frequency import psd_multitaper, psd_welch
from mne.viz import plot_topomap
import matplotlib.pyplot as plt
from numpy import mean

class RawPSD :
    #--------------------------------------------------------------------------------------------------------
    def __init__(self, raw, fmin = 0, fmax = 1500, tmin = None, tmax = None, method = 'multitaper', **kwargs) :
        """
        Computes the PSD of the raw file with the correct method multitaper or welch.

        Arguments :
        ============
        raw (mne Raw)               : Instance of Raw to be processed
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

        self.info            = raw.info
        self.method          = method

        self.bandwidth = kwargs.get('bandwidth', 4.)
        self.n_fft     = kwargs.get('n_fft', 256)
        self.n_per_seg = kwargs.get('n_per_seg', self.n_fft)
        self.n_overlap = kwargs.get('n_overlap', 0)


        if method == 'multitaper' :
            print("Computing Mulitaper PSD with parameter bandwidth = {}".format(self.bandwidth))
            self.data, self.freqs = psd_multitaper(raw,
                                                   fmin             = fmin,
                                                   fmax             = fmax,
                                                   tmin             = tmin,
                                                   tmax             = tmax,
                                                   normalization    = 'full',
                                                   bandwidth        = self.bandwidth)

        if method == 'welch'      :
            print("Computing Welch PSD with parameters n_fft = {}, n_per_seg = {}, n_overlap = {}".format(
                  self.n_fft, self.n_per_seg, self.n_overlap))
            self.data, self.freqs = psd_welch(raw,
                                              fmin      = fmin,
                                              fmax      = fmax,
                                              tmin      = tmin,
                                              tmax      = tmax,
                                              n_fft     = self.n_fft,
                                              n_overlap = self.n_overlap,
                                              n_per_seg = self.n_per_seg)

    #--------------------------------------------------------------------------------------------------------
    def plot_topomap(self, freq_index, axes = None, show_names = False) :
        """
        Plot the map of the power for a given frequency chosen by freq_index, the frequency
        is hence the value self.freqs[freq_index]. This function will return an error if the class
        is not initialized with the coordinates of the different electrodes.

        Arguments :
        ============
        freq_index (int)            : index of the frequency in self.freqs
        axes (axe)                  : Instance of matplotlib Axes
        show_names (bool)           : show names on topomap (needs names in file)

        Returns :
        ============
        Instance of Matplotlib.Image
        """
        # Handling error if no coordinates are found
        if self.info['chs'][0]['loc'] is None :
            raise ValueError("No locations available for this dataset")

        psd_values = self.data[:, freq_index]
        return plot_topomap(psd_values, self.info, axes = axes, show = False, cmap = 'GnBu', show_names = show_names)

    #--------------------------------------------------------------------------------------------------------
    def plot_topomap_band(self, freq_index_min, freq_index_max, axes = None, vmin = None, vmax = None, show_names = False) :
        """
        Plot the map of the power for a given frequency band chosen by freq_index_min and freq_index_max
        , the frequency is hence the value self.freqs[freq_index]. This function will return an error if
        the class is not initialized with the coordinates of the different electrodes.

        Arguments :
        ============
        freq_index_max (int)        : index of the min frequency in self.freqs
        freq_index_min (int)        : index of the max frequency in self.freqs
        axes           (axe)        : Instance of matplotlib Axes
        vmin           (float)      : Maximum value of power to display
        vmax           (float)      : Minimum value of power to display
        show_names     (bool)       : show names on topomap (needs names in file)

        Returns :
        ============
        Instance of Matplotlib.Image
        """
        # Handling error if no coordinates are found
        if self.info['chs'][0]['loc'] is None :
            raise ValueError("No locations available for this dataset")

        psd_values = self.data[:, freq_index_min : freq_index_max]
        psd_mean = mean(psd_values, axis = 1)
        return plot_topomap(psd_mean, self.info, axes = axes, vmin = vmin, vmax = vmax, show = False, cmap = 'GnBu', show_names = show_names)

    #--------------------------------------------------------------------------------------------------------
    def plot_matrix(self, freq_index_min, freq_index_max, axes = None, vmin = None, vmax = None) :
        """
        Plot the map of the average power for a given frequency band chosen by freq_index_min and
        freq_index_max, the frequency is hence the value self.freqs[freq_index]. This function will
        return an error if the class is not initialized with the coordinates of the different
        electrodes.

        Arguments :
        ============
        freq_index_max (int)        : index of the min frequency in self.freqs
        freq_index_min (int)        : index of the max frequency in self.freqs
        axes           (axe)        : Instance of matplotlib Axes
        vmin           (float)      : Maximum value of power to display
        vmax           (float)      : Minimum value of power to display

        Returns :
        ============
        Instance of Matplotlib.Image
        """
        extent = [self.freqs[freq_index_min], self.freqs[freq_index_max], self.data.shape[0] + 1, 1]
        mat = self.data[:, freq_index_min : freq_index_max]
        if axes is not None :
            return axes.matshow(mat, extent = extent, cmap = 'GnBu', vmin = vmin, vmax = vmax)
        else :
            return plt.matshow(mat, extent = extent, cmap = 'GnBu', vmin = vmin, vmax = vmax)

    #--------------------------------------------------------------------------------------------------------
    def plot_single_psd(self, channel_index, freq_index_min, freq_index_max, axes = None) :
        """
        Plot a single PSD corresponding channel_index, between the values corresponding
        to freq_index_max and freq_index_min.

        Arguments :
        ============
        channel_index  (int)        : index of the channel to display
        freq_index_max (int)        : index of the min frequency in self.freqs
        freq_index_min (int)        : index of the max frequency in self.freqs
        axes           (axe)        : Instance of matplotlib Axes

        Returns :
        ============
        Instance of Matplotlib.Image
        """
        psd = self.data[channel_index, freq_index_min : freq_index_max]
        if axes is not None :
            return axes.plot(self.freqs[freq_index_min : freq_index_max], psd)
        else :
            return plt.plot(self.freqs[freq_index_min : freq_index_max], psd)


    def save_matrix_txt(self, path, freq_index_min = 0, freq_index_max = -1) :
        """
        Save the entire matrix as a raw txt-file containing the data of the matrix
        """
        from numpy import savetxt
        data = self.data[:, freq_index_min:freq_index_max]
        savetxt(path, data)
