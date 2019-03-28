import matplotlib.pyplot as plt
from numpy import log

class RawPSD :
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
    plot_avg_topomap_band       : Plot the map of the power for a given band, averaged over epochs
    plot_matrix                 : Plot the raw matrix
    plot_single_psd             : Plot the PSD for a given epoch and channel
        """
    #--------------------------------------------------------------------------------------------------------
    def __init__(self, raw, fmin = 0, fmax = 1500, tmin = None, tmax = None, method = 'multitaper', **kwargs) :
        """
        Computes the PSD of the raw file with the correct method multitaper or welch.
        """
        self.fmin, self.fmax = fmin, fmax
        self.tmin, self.tmax = tmin, tmax

        self.info            = raw.info
        self.method          = method

        self.bandwidth = kwargs.get('bandwidth', 4.)
        self.n_fft     = kwargs.get('n_fft', 256)
        self.n_per_seg = kwargs.get('n_per_seg', self.n_fft)
        self.n_overlap = kwargs.get('n_overlap', 0)
        self.cmap = 'inferno'

        if method == 'multitaper' :
            from mne.time_frequency import psd_multitaper

            print("Computing Mulitaper PSD with parameter bandwidth = {}".format(self.bandwidth))
            self.data, self.freqs = psd_multitaper(raw,
                                                   fmin             = fmin,
                                                   fmax             = fmax,
                                                   tmin             = tmin,
                                                   tmax             = tmax,
                                                   normalization    = 'full',
                                                   bandwidth        = self.bandwidth)

        if method == 'welch'      :
            from mne.time_frequency import psd_welch

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
    def plot_topomap(self, freq_index, axes = None, log_display = False) :
        """
        Plot the map of the power for a given frequency chosen by freq_index, the frequency
        is hence the value self.freqs[freq_index]. This function will return an error if the class
        is not initialized with the coordinates of the different electrodes.
        """
        from mne.viz import plot_topomap

        # Handling error if no coordinates are found
        if self.info['chs'][0]['loc'] is None :
            raise ValueError("No locations available for this dataset")

        psd_values = self.data[:, freq_index]
        if log_display : psd_values = 10 * log(psd_values)
        return plot_topomap(psd_values, self.info, axes = axes, show = False, cmap = self.cmap)

    #--------------------------------------------------------------------------------------------------------
    def plot_topomap_band(self, freq_index_min, freq_index_max, axes = None, vmin = None, vmax = None, log_display = False) :
        """
        Plot the map of the power for a given frequency band chosen by freq_index_min and freq_index_max
        , the frequency is hence the value self.freqs[freq_index]. This function will return an error if
        the class is not initialized with the coordinates of the different electrodes.
        """
        from mne.viz import plot_topomap
        from numpy import mean

        # Handling error if no coordinates are found
        if self.info['chs'][0]['loc'] is None :
            raise ValueError("No locations available for this dataset")

        psd_values = self.data[:, freq_index_min : freq_index_max]
        psd_mean = mean(psd_values, axis = 1)
        if log_display : psd_mean = 10 * log(psd_mean)
        return plot_topomap(psd_mean, self.info, axes = axes, vmin = vmin, vmax = vmax, show = False, cmap = self.cmap)

    #--------------------------------------------------------------------------------------------------------
    def plot_matrix(self, freq_index_min, freq_index_max, axes = None, vmin = None, vmax = None, log_display = False) :
        """
        Plot the map of the average power for a given frequency band chosen by freq_index_min and
        freq_index_max, the frequency is hence the value self.freqs[freq_index]. This function will
        return an error if the class is not initialized with the coordinates of the different
        electrodes.
        """
        extent = [self.freqs[freq_index_min], self.freqs[freq_index_max], self.data.shape[0] + 1, 1]
        mat = self.data[:, freq_index_min : freq_index_max]
        if log_display : mat = 10 * log(mat)
        if axes is not None :
            return axes.matshow(mat, extent = extent, cmap = self.cmap, vmin = vmin, vmax = vmax)
        else :
            return plt.matshow(mat, extent = extent, cmap = self.cmap, vmin = vmin, vmax = vmax)

    #--------------------------------------------------------------------------------------------------------
    def plot_single_psd(self, channel_index, freq_index_min, freq_index_max, axes = None, log_display = False) :
        """
        Plot a single PSD corresponding channel_index, between the values corresponding
        to freq_index_max and freq_index_min.
        """
        psd = self.data[channel_index, freq_index_min : freq_index_max]
        if log_display : psd = 10 * log(psd)
        if axes is not None :
            return axes.plot(self.freqs[freq_index_min : freq_index_max], psd)
        else :
            return plt.plot(self.freqs[freq_index_min : freq_index_max], psd)

    #--------------------------------------------------------------------------------------------------------
    def save_matrix_txt(self, path, freq_index_min = 0, freq_index_max = -1) :
        """
        Save the entire matrix as a raw txt-file containing the data of the matrix
        """
        from numpy import savetxt
        data = self.data[:, freq_index_min:freq_index_max]
        savetxt(path, data)
