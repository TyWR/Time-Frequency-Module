FROM ubuntu:18.04
# Install Python 3, PyQt5
RUN apt-get update
RUN apt-get install -y tzdata
RUN apt-get install -y python3
RUN apt-get install -y python3-pyqt5
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-tk
RUN apt-get install -y libxkbcommon-x11-dev

#Install python libraries
COPY requirements.txt main/requirements.txt
RUN python3 -m pip install -r main/requirements.txt

#Copy all the files
COPY backend main/backend
COPY media main/media
COPY run_app.py main/run_app.py
COPY app main/app

WORKDIR /main
CMD [ "python3", "run_app.py" ]
