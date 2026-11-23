# Smart Fridge

A system that watches my fridge and knows which staples are usually there. When I ask from my phone, it shows me the latest photo of the fridge and which staples look missing or low. It runs on my own old laptops.

## Why

I run out of staples and only notice when I need them. I also want hands-on experience with infrastructure, data pipelines, edge devices, and ML systems, so this project is built to need all of them.

## First archiecture I am thinking right now. 

A sensor on the fridge door, like an ESP32 with a reed switch, which publishes an event over MQTT to a broker whenever the door opens or closes. When the door closes, a camera takes a snapshot and the image is saved to object storage. Saving the image triggers a "new snapshot" event, which tells a vision worker to look at the photo and detect which items are in it. Those detections are written to a time-series database. An inventory service reads that history and compares it against what's usually in the fridge. When I open the app on my phone, it returns the latest photo and the list of staples that look missing.