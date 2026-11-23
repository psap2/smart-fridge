# Smart Fridge

A system that watches my fridge, knows which staples are usually there, and alerts my phone when something looks missing or low. It runs on my own old laptops.

## Why

I run out of staples and only notice when I need them. I also want hands-on experience with infrastructure, data pipelines, edge devices, and ML systems, so this project is built to need all of them.

## First archiecture I am thinking right now. 

A sensor on the fridge door, like an ESP32 with a reed switch, which publishes an event over MQTT to a broker whenever the door opens or closes. When the door closes, a camera takes a snapshot and the image is saved to object storage. Saving the image triggers a "new snapshot" event, which tells a vision worker to look at the photo and detect which items are in it. Those detections are written to a time-series database. An inventory service reads that history, compares it against what's usually in the fridge, and sends an alert to my phone when a staple looks missing or low.
