# Time-Frequency-Module

## This is an old personal repository, please checkout here : https://github.com/fcbg-hnp/eeg-timeFreqToolbox

Development of Time-Frequency module for EEG signal processing, using the library MNE and Qt.

[MNE Library Link](https://martinos.org/mne/dev/index.html)

# Installation 

You must have python 3 installed. 

To install the dependencies required for this application, run the line `pip install -r requirements.txt`

To launch the app, simply run the `run_app.py` file.

For now, the app can only treat the data to display the power spectrum density of raw eeg files, and epoched eeg files, with the formats `.fif`, `.sef`, `.ep` and `.eph`.

## Docker building and running

After building the docker image with the dockerfile, you can run the app with the line : `sudo docker run -it -v /tmp/.X11-unix:/tmp/.X11-unix -v /datapath:/data -e DISPLAY=unix$DISPLAY myapp` on Ubuntu. 

## Quick Tutorial

![Main Window](https://github.com/TyWR/Time-Frequency-Module/blob/master/media/main_window.png)

First import your file which can be either a raw file (format `*.fif` or `*.sef`), or epoched data (format `.epo-fif`).

The application also comes with an handy tool to process raw data files into epochs data with the help of a marker file (of format `*.mrk`). Just click on the `Cut into Epochs` button, and save your epochs data as a `*-epo.fif` file.

 For the topomaps plot you can either choose premade electrode setting from `mne` (If your file comes with corresponding 1005 or 1020 system names), or import the `*.xyz` file containing the 3D coordinates of the data in the electrode labeling menu.

 Then you have two choice of data visualization :

 * **PSD (Power Spectrum Density)** : Which computes the power spectrum density of the signal. You can display the results either in the form of a matrix (Simple plot of individual Channels by Frequencies), or as a topomap (Power of electrode represented on the scalp). It is also possible to run across the different epochs if the file is epoched data.

 * **Average TFR (Average Time-Frequency)** : Which computes the time-frequency representation of the signal averaged over epochs. This feature only works on epoched data. You can either display the results on regular time-frequency representation (Time by Frequency), or displays it in differents ways channels by frequencies, or channels by time.


## Parameters handling

You can easily import parameters using the import button in the app. The parameters are setup in a simple txt file, in the following way :

`param_id = value` or `param_id = value1, value2, ...` if several values are expected.

Check here for a detailed description of parameters : [Click Here !](https://github.com/TyWR/Time-Frequency-Module/blob/master/media/help_parameters.md)
