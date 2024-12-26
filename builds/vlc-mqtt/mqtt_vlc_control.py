import os
import subprocess
import paho.mqtt.client as mqtt
import time

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USER", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")

TOPIC_LOCAL_SOUND = os.getenv("TOPIC_LOCAL_SOUND", "vlc/play/local")
TOPIC_STREAM = os.getenv("TOPIC_STREAM", "vlc/play/stream")
TOPIC_REMOTE_SOUND = os.getenv("TOPIC_REMOTE_SOUND", "vlc/play/remote")
TOPIC_STATUS = os.getenv("TOPIC_STATUS", "vlc/status")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT broker: {MQTT_BROKER}")

        client.publish(TOPIC_STATUS, "connected")
        client.subscribe([(TOPIC_LOCAL_SOUND, 0), (TOPIC_STREAM, 0), (TOPIC_REMOTE_SOUND, 0)])
    else:
        print(f"Failed to connect to MQTT broker, return code {rc}")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker.")
    client.publish(TOPIC_STATUS, "disconnected")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()

    if topic == TOPIC_LOCAL_SOUND:
        local_file = os.path.join("/opt/sounds", payload)
        if os.path.exists(local_file):
            print(f"Playing local sound file: {local_file}")
            subprocess.run(["cvlc", "--intf=dummy", "--aout=dummy", "--no-video", local_file])
        else:
            print(f"Local file not found: {local_file}")
    elif topic == TOPIC_STREAM:
        print(f"Playing stream URL: {payload}")
        subprocess.run(["cvlc", "--intf=dummy", "--aout=dummy", "--no-video", payload])
    elif topic == TOPIC_REMOTE_SOUND:
        print(f"Playing remote sound file: {payload}")
        subprocess.run(["cvlc", "--intf=dummy", "--aout=dummy", "--no-video", payload])

client = mqtt.Client()

if MQTT_USER and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    print(f"Listening on topics: {TOPIC_LOCAL_SOUND}, {TOPIC_STREAM}, {TOPIC_REMOTE_SOUND}")
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")
    exit(1)


while True:
    time.sleep(1)

