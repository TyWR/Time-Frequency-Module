# Time-Frequency-Module
Development of Time-Frequency module for EEG signal processing, using the library MNE and Qt.

[MNE Library Link](https://martinos.org/mne/dev/index.html)

To launch the app, simply run the `run_app.py` file.

For now, the app can only treat the data to display the power spectrum density of raw eeg files, and epoched eeg files, with the formats `.fif`, `.sef`, `.ep` and `.eph`.

After building the docker image with the dockerfile, you can run the app with the line : `docker run -it/tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY docker_image_name`. 


