"""
Listens for door events on the MQTT broker and counts door closes.
On every 5th close it publishes a "take a photo" request
"""
import json
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
DOOR_TOPIC = "fridge/door"        # where door events arrive
CAPTURE_TOPIC = "fridge/capture"  # where photo requests are sent
CLOSES_PER_PHOTO = 5

# How many closes have been seen since the last photo request.
# This lives in memory only, so it starts again from 0 if the listener restarts.
closes_since_photo = 0


def on_connect(client, userdata, flags, reason_code, properties):
    """Runs once the broker accepts the connection."""
    print(f"Connected to broker, listening on {DOOR_TOPIC}")
    # Subscribing here means the subscription is set up again after a reconnect.
    client.subscribe(DOOR_TOPIC)


def on_message(client, userdata, msg):
    """Runs every time a message arrives on a topic we subscribed to."""
    global closes_since_photo

    # The message arrives as bytes. Turn it back into the event dictionary.
    try:
        event = json.loads(msg.payload)
        state = event["state"]
    except (ValueError, KeyError, TypeError):
        # Not valid JSON, or no "state" in it. Skip it rather than crash.
        print(f"Ignored a message I couldn't read: {msg.payload!r}")
        return

    print(f"Door event: {state} at {event.get('time')}")

    # Only closes count. Opens are printed and otherwise ignored.
    if state != "closed":
        return

    closes_since_photo += 1
    print(f"  closes since last photo: {closes_since_photo}/{CLOSES_PER_PHOTO}")

    if closes_since_photo >= CLOSES_PER_PHOTO:
        request = {
            "requested_by": "door-listener",
            "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        client.publish(CAPTURE_TOPIC, json.dumps(request))
        print(f"  published photo request to {CAPTURE_TOPIC}")
        closes_since_photo = 0


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER_HOST, BROKER_PORT)

# Wait for messages forever, calling on_message for each one.
try:
    client.loop_forever()
except KeyboardInterrupt:
    client.disconnect()
    print("\nStopped.")
