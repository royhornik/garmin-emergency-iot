# IoT Real-Time Emergency Alert System

An end-to-end IoT emergency response system linking Garmin wearable hardware, an asynchronous edge application, and a cloud backend to trigger automated telephony alerts.

## Architecture
1. **Edge (Garmin Watch):** Developed in Monkey C using Connect IQ SDK. Samples heart rate asynchronously (Event-Driven) and includes state-based debounce logic to avoid alert flooding.
2. **Backend (Server):** Python (Flask) REST API that ingests JSON payloads from the watch.
3. **Telephony (Twilio):** Converts alert triggers into automated outbound VoIP calls with Text-to-Speech synthesis.

## Tech Stack
* **Firmware:** Monkey C, Garmin Connect IQ SDK
* **Backend:** Python, Flask, REST APIs
* **Networking & Cloud:** ngrok (tunneling), Twilio Voice API