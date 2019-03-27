from matplotlib.pyplot import imshow


class AvgEpochsTFR :
    """
    Class to handle the Time-Frequency data of epochs

    self.tfr.data of shape (n_channels, n_freqs, n_times)
    """
    def __init__(self, epochs, freqs, n_cycles, method = 'multitaper', time_bandwidth = 4., n_fft = 512, width = 1, picks = None) :
        """Initialize the class with an instance of EpochsTFR corresponding to the method"""
        self.picks = picks
        if method == 'multitaper' :
            from mne.time_frequency import tfr_multitaper
            self.tfr, _ = tfr_multitaper(epochs, freqs, n_cycles, time_bandwidth = time_bandwidth, picks = picks)

        if method == 'stockwell'  :
            from mne.time_frequency import tfr_stockwell
            self.tfr, _ = tfr_stockwell(epochs, freqs, n_cycles, n_fft = n_fft, width = width, picks = picks)

        if method == 'morlet'     :
            from mne.time_frequency import tfr_morlet
            self.tfr, _ = tfr_morlet(epochs, freqs, n_cycles, picks = picks)

    def plot_time_freq(self, index_channel, ax, vmax = None) :
        """Plot the averaged epochs time-frequency plot for a given channel"""
        data = self.tfr.data[index_channel, :, :]
        extent = [self.tfr.times[0], self.tfr.times[-1],
                  self.tfr.freqs[0], self.tfr.freqs[-1]]
        return ax.imshow(data, extent = extent, aspect = 'auto', origin = 'lower', vmax = vmax)

    def plot_freq_ch(self, time_index, ax, vmax = None) :
        """Plot the averaged epochs frequency-channel plot for a given time"""
        data = self.tfr.data[:, :, time_index]
        extent = [self.tfr.freqs[0], self.tfr.freqs[-1],
                                 .5, len(self.picks)+.5]
        return ax.imshow(data, extent = extent, aspect = 'auto', origin = 'lower', vmax = vmax)

    def plot_time_ch(self, freq_index, ax, vmax = None) :
        """Plot the averaged epochs time-channel plot for a given frequency range"""
        data = self.tfr.data[:, freq_index, :]
        extent = [self.tfr.times[0], self.tfr.times[-1],
                                 .5, len(self.picks)+.5]
        return ax.imshow(data, extent = extent, aspect = 'auto', origin = 'lower', vmax = vmax)
