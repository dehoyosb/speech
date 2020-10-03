FROM pytorch/pytorch:0.4.1-cuda9-cudnn7-devel

WORKDIR /workspace

RUN apt-get update -y && \
    #apt-get -y upgrade && \
    apt install -y build-essential && \
    apt-get install -y manpages-dev && \
    apt install -y ffmpeg && \
    apt-get install -y \
    libsndfile-dev \
    portaudio19-dev \
    festival \
    git \
    mbrola
    #espeak-ng

RUN pip install Cython \
    cffi==1.11.2 \
    editdistance==0.3.1 \
    numpy==1.13.3 \
    protobuf==3.4.0 \
    py==1.4.34 \
    pycparser==2.18 \
    pytest==3.2.3 \
    scipy==0.18.1 \
    six==1.11.0 \ 
    SoundFile==0.10.2 \
    tensorboard-logger==0.0.4 \
    tqdm==4.19.4 \
    phonemizer

#RUN git clone https://github.com/dehoyosb/speech.git && \
#    cd /speech && \
#    source setup.sh && \
#    cd example/common_voice

#CMD [ "/bin/bash", "-c", "data_prep.sh", $data/clip_original]
