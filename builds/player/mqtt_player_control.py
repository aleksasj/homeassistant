import os
import subprocess
import paho.mqtt.client as mqtt
import time

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USER", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")


print(f"VLC MQTT started")
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT broker: {MQTT_BROKER}")

        client.publish("player/status", "connected")
        client.subscribe([("player/play", 0)])
    else:
        print(f"Failed to connect to MQTT broker, return code {rc}")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker.")
    client.publish("player/status", "disconnected")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"Topic: {topic}, Payload: {payload}")

    if topic == "player/play":
        if not payload.startswith("http"):
            payload = os.path.join("/opt/sounds", payload)
        play_audio_thread(paylod)

def play_sound(payload):
    try:
        subprocess.run(['play', payload])
        print(f"Playing audio from source {payload}")
    except Exception as e:
        print(f"Failed to play audio from source {payload}")


def play_audio_thread(payload):
    global current_thread

    if current_thread and current_thread.is_alive():
        current_thread.join(timeout=1)

    current_thread = threading.Thread(target=play_sound, args=(payload,))
    current_thread.start()


client = mqtt.Client()

if MQTT_USER and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

try:
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.loop_start()
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")
    exit(1)


while True:
    time.sleep(1)

