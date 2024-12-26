FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y \
    vlc \
    python3 \
    python3-pip \
    python3-venv \
    alsa-utils \
    && apt-get clean

RUN python3 -m venv /opt/venv

RUN apt-get install -y python3-paho-mqtt

RUN useradd -m vlcuser

ENV PATH="/root/.local/bin:$PATH"

RUN mkdir -p /opt/sounds && chown -R vlcuser:vlcuser /opt/sounds

COPY mqtt_vlc_control.py /opt/mqtt_vlc_control.py
RUN chmod +x /opt/mqtt_vlc_control.py

RUN chown vlcuser:vlcuser /opt/mqtt_vlc_control.py && chmod +x /opt/mqtt_vlc_control.py

USER vlcuser

WORKDIR /opt

ENTRYPOINT ["python3", "/opt/mqtt_vlc_control.py"]
