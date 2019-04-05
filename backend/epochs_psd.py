import matplotlib.pyplot as plt
from numpy import mean, log

class EpochsPSD :
    """
    This class contains the PSD of a set of Epochs. It stores the data of
    the psds of each epoch. The psds are calculated with the Library mne.

    Attributes :
    ============
    fmin        (float)         : frequency limit

    fmax        (float)         : frequency limit

    tmin        (float)         : lower time bound for each epoch

    tmax        (float)         : higher time bound for each epoch

    info        (mne Infos)     : info of the epochs

    method      (str)           : method used for PSD (multitaper or welch)

    data        (numpy arr.)    : dataset with all the psds data of size
                                  (n_epochs, n_channels, n_freqs)

    freqs       (arr.)          : list containing the frequencies of the psds

    Methods :
    ============
    __init__                    : Compute all the PSD of each epoch

    plot_topomap                : Plot the map of the power for a given
                                  frequency and epoch

    plot_topomap_band           : Plot the map of the power for a given band
                                  frequency and epoch

    plot_avg_topomap_band       : Plot the map of the power for a given band,
                                  averaged over epochs

    plot_avg_matrix             : Plot the raw matrix

    plot_avg                    : Plot the matrix for a given epoch

    plot_single_psd             : Plot the PSD for a given epoch and channel

    plot_single_avg_psd         : Plot the PSD averaged over epochs for a given chanel
    """

    #------------------------------------------------------------------------
    def __init__(self, epochs, fmin = 0, fmax = 1500,
                 tmin = None, tmax = None,
                 method = 'multitaper', picks = None, **kwargs) :
        """
        Computes the PSD of the epochs with the correct method multitaper or welch
        """
        # Create a a sub instance of raw with the picked channels
        if picks is not None :
            ch_names = [epochs.info['ch_names'][i] for i in picks]
            self.picked_info = epochs.copy().pick_channels(ch_names).info
        else :
            self.picked_info = epochs.info

        self.fmin, self.fmax    = fmin, fmax
        self.tmin, self.tmax    = tmin, tmax
        self.info               = epochs.info
        self.method             = method
        self.bandwidth          = kwargs.get('bandwidth', 4.)
        self.n_fft              = kwargs.get('n_fft', 256)
        self.n_per_seg          = kwargs.get('n_per_seg', self.n_fft)
        self.n_overlap          = kwargs.get('n_overlap', 0)
        self.picks              = picks
        self.cmap               = 'inferno'


        if method == 'multitaper' :
            from mne.time_frequency import psd_multitaper

            print("Computing Mulitaper PSD with parameter bandwidth = {}"
            .format(self.bandwidth))
            self.data, self.freqs = psd_multitaper(
                epochs,
                fmin             = fmin,
                fmax             = fmax,
                tmin             = tmin,
                tmax             = tmax,
                normalization    = 'full',
                bandwidth        = self.bandwidth,
                picks            = picks)

        if method == 'welch'      :
            from mne.time_frequency import psd_welch

            print("Computing Welch PSD with parameters"
                  + " n_fft = {}, n_per_seg = {}, n_overlap = {}"
                  .format(self.n_fft, self.n_per_seg, self.n_overlap))
            self.data, self.freqs = psd_welch(
                epochs,
                fmin      = fmin,
                fmax      = fmax,
                tmin      = tmin,
                tmax      = tmax,
                n_fft     = self.n_fft,
                n_overlap = self.n_overlap,
                n_per_seg = self.n_per_seg,
                picks     = picks)

    #------------------------------------------------------------------------
    def __str__(self) :
        """Return informations about the instance"""

        string = ("PSD Computed on {} Epochs with method {}.\nParameters : \n"
                 + "fmin:{}Hz, fmax:{}Hz (with {} frequency points)\n"
                 + "tmin : {}s, tmax : {}s\n")
        string.format(len(self.info['chs']), self.method,
                      self.fmin, self.fmax, len(self.freqs),
                      self.tmin, self.tmax)
        if self.method == 'welch' :
            string = (string + "n_fft:{}, n_per_seg:{}, n_overlap:{}\n")
            string.format(self.n_fft, self.n_per_seg, self.n_overlap)
        else :
            string = string + "bandwidth:{}".format(self.bandwidth)
        return string

    #------------------------------------------------------------------------
    def recap(self) :
        """Returns a quick recap"""

        if self.method == 'welch' :
            string = ("Computed with Welch method, "
                     + "n_fft : {}, n_per_seg : {}, n_overlap : {}\n")
            string.format(self.n_fft, self.n_per_seg, self.n_overlap)
        else :
            string = "Computed with Multitaper method, bandwidth : {}"
            string.format(self.bandwidth)
        return string

    #------------------------------------------------------------------------
    def plot_topomap(self, epoch_index, freq_index,
                     axes = None, log_display = False,
                     head_pos = None) :
        """
        Plot the map of the power for a given frequency chosen by freq_index,
        the frequencyis hence the value self.freqs[freq_index]. This function
        will return an error if the class is not initialized with the
        coordinates of the different electrodes.
        """
        from mne.viz import plot_topomap

        psd_values = self.data[epoch_index, :, freq_index]
        if log_display : psd_values = 10 * log(psd_values)
        return plot_topomap(psd_values, self.picked_info, axes = axes,
                            show = False, cmap = self.cmap,
                            head_pos = head_pos)

    #------------------------------------------------------------------------
    def plot_topomap_band(self, epoch_index, freq_index_min, freq_index_max,
                          axes = None, vmin = None, vmax = None,
                          log_display = False, head_pos = None) :
        """
        Plot the map of the power for a given frequency band chosen by
        freq_index_min and freq_index_max, the frequency is hence the value
        self.freqs[freq_index]. This function will return an error if the
        class is not initialized with the coordinates of the different
        electrodes.
        """
        from mne.viz import plot_topomap

        psd_values = self.data[epoch_index, :, freq_index_min : freq_index_max]
        psd_mean = mean(psd_values, axis = 1)
        if log_display : psd_mean = 10 * log(psd_mean)
        return plot_topomap(psd_mean, self.picked_info, axes = axes,
                            vmin = vmin, vmax = vmax, show = False,
                            cmap = self.cmap, head_pos = head_pos)

    #------------------------------------------------------------------------
    def plot_avg_topomap_band(self, freq_index_min, freq_index_max,
                              vmin = None, vmax = None, show_names = False,
                              log_display = False, axes = None,
                              head_pos = None) :
        """
        Plot the map of the average power for a given frequency band chosen
        by freq_index_min and freq_index_max, the frequency is hence the value
        self.freqs[freq_index]. This function will return an error if the
        class is not initialized with the coordinates of the different
        electrodes.
        """
        from mne.viz import plot_topomap

        psd_values = self.data[:, :, freq_index_min : freq_index_max]
        psd_mean = mean(psd_values, axis = 2)  #average over frequency band
        psd_mean = mean(psd_mean,   axis = 0)  #average over epochs
        if log_display : psd_mean = 10 * log(psd_mean)
        return plot_topomap(psd_mean, self.picked_info, axes = axes,
                            vmin = vmin, vmax = vmax, show = False,
                            cmap = self.cmap, head_pos = head_pos)

    #------------------------------------------------------------------------
    def plot_avg_matrix(self, freq_index_min, freq_index_max, axes = None,
                        vmin = None, vmax = None, log_display = False) :
        """
        Plot the map of the average power for a given frequency band chosen
        by freq_index_min and freq_index_max, the frequency is hence the value
        self.freqs[freq_index]. This function will return an error if the
        class is not initialized with the coordinates of the different
        electrodes.
        """
        extent = [
            self.freqs[freq_index_min], self.freqs[freq_index_max],
                self.data.shape[1] + 1,                          1
        ]
        mat = mean(self.data[:, :, freq_index_min : freq_index_max], axis = 0)
        if log_display : mat = 10 * log(mat)
        if axes is not None :
            return axes.matshow(mat, extent = extent, cmap = self.cmap,
                                vmin = vmin, vmax = vmax)
        else :
            return plt.matshow(mat, extent = extent, cmap = self.cmap,
                               vmin = vmin, vmax = vmax)

    #--------------------------------------------------------------------------
    def plot_matrix(self, epoch_index, freq_index_min, freq_index_max,
                    axes = None, vmin = None, vmax = None,
                    log_display=False) :
        """
        Plot the map of the average power for a given frequency band chosen
        by freq_index_min and freq_index_max, the frequency is hence the value
        self.freqs[freq_index]. This function will return an error if the
        class is not initialized with the coordinates of the different
        electrodes.
        """
        extent = [
            self.freqs[freq_index_min], self.freqs[freq_index_max],
                self.data.shape[1] + 1,                          1
        ]
        mat = self.data[epoch_index, :, freq_index_min : freq_index_max]
        if log_display : mat = 10 * log(mat)
        if axes is not None :
            return axes.matshow(mat, extent = extent, cmap = self.cmap,
                                vmin = vmin, vmax = vmax)
        else :
            return plt.matshow(mat, extent = extent, cmap = self.cmap,
                               vmin = vmin, vmax = vmax)

    #--------------------------------------------------------------------------
    def plot_single_psd(self, epoch_index, channel_index,
                        freq_index_min, freq_index_max,
                        axes = None, log_display = False) :
        """
        Plot a single PSD corresponding to epoch_index and channel_index,
        between the values corresponding to freq_index_max and
        freq_index_min.
        """
        psd = self.data[epoch_index, channel_index,
                        freq_index_min : freq_index_max]
        if log_display : psd = 10 * log(psd)
        if axes is not None :
            return axes.plot(self.freqs[freq_index_min : freq_index_max], psd)
        else :
            return plt.plot(self.freqs[freq_index_min : freq_index_max], psd)

    #--------------------------------------------------------------------------
    def plot_single_avg_psd(self, channel_index,
                            freq_index_min, freq_index_max,
                            axes = None, log_display = False) :
        """
        Plot a single PSD averaged over epochs and corresponding to
        channel_index, between the values corresponding to freq_index_max
        and freq_index_min.
        """
        psd = mean(self.data[:, channel_index,
                             freq_index_min : freq_index_max], axis = 0)
        if log_display : psd = 10 * log(psd)
        if axes is not None :
            return axes.plot(self.freqs[freq_index_min : freq_index_max], psd)
        else :
            return plt.plot(self.freqs[freq_index_min : freq_index_max], psd)

    #--------------------------------------------------------------------------
    def save_matrix_txt(self, path) :
        print("SHOULD SAVE MATRIX FOR EPOCHS")

    #--------------------------------------------------------------------------
    def save_avg_matrix_sef(self, path) :
        """
        Save the entire matrix in a sef file
        """
        import numpy as np
        import struct

        n_channels = len(self.info['ch_names'])
        num_freq_frames = len(self.freqs)
        freq_step = (self.freqs[-1] - self.freqs[0]) / num_freq_frames
        sfreq = float(1 / freq_step)

        f = open(path, 'wb')
        for car in 'SE01' :
            f.write(struct.pack('c', bytes(car, 'ASCII')))
        f.write(struct.pack('I', n_channels))
        f.write(struct.pack('I', 0))
        f.write(struct.pack('I', num_freq_frames))
        f.write(struct.pack('f', sfreq))
        f.write(struct.pack('H', 0))
        f.write(struct.pack('H', 0))
        f.write(struct.pack('H', 0))
        f.write(struct.pack('H', 0))
        f.write(struct.pack('H', 0))
        f.write(struct.pack('H', 0))
        f.write(struct.pack('H', 0))

        for name in self.info['ch_names'] :
            n = 0
            for car in name :
                f.write(struct.pack('c', bytes(car, 'ASCII')))
                n += 1
            while n < 8 :
                f.write(struct.pack('x'))
                n += 1

        data = self.data.astype(np.float32)
        data = np.reshape(np.mean(data, axis = 0),
                          n_channels * num_freq_frames,
                          order = 'F')
        data.tofile(f)
        f.close()
        print("done !")
