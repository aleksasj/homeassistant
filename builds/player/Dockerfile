FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y \
    sox \
    python3-paho-mqtt \
    python3 \
    python3-pip \
    python3-venv \
    alsa-utils \
    && apt-get clean

RUN python3 -m venv /opt/venv

RUN useradd -m vlcuser && usermod -aG audio vlcuser

ENV PATH="/root/.local/bin:$PATH"

RUN mkdir -p /opt/sounds && chown -R vlcuser:vlcuser /opt/sounds

COPY mqtt_player_control.py /opt/mqtt_player_control.py
RUN chmod +x /opt/mqtt_player_control.py

RUN chown vlcuser:vlcuser /opt/mqtt_player_control.py && chmod +x /opt/mqtt_player_control.py

USER vlcuser

WORKDIR /opt

ENTRYPOINT ["python3", "/opt/mqtt_player_control.py"]
