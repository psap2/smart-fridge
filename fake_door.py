"""
Publishes a door event to the MQTT broker. A way to mock the real door
sensor so the subscribers that listen for door events can be tested
without hardware.
"""
import json
import sys
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"  
BROKER_PORT = 1883
TOPIC = "fridge/door"
SENSOR_NAME = "fridge-door"

state = sys.argv[1] if len(sys.argv) > 1 else "closed"
if state not in ("open", "closed"):
    sys.exit(f"State must be 'open' or 'closed', not '{state}'")

event = {
    "sensor": SENSOR_NAME,
    "state": state,
    "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
}

message = json.dumps(event)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER_HOST, BROKER_PORT)
client.loop_start()
client.publish(TOPIC, message).wait_for_publish(timeout=5)
client.loop_stop()
client.disconnect()
print(f"Published to {TOPIC}: {message}")
