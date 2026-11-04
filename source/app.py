from flask import Flask, request, jsonify
from twilio.rest import Client

app = Flask(__name__)

# Twilio credentials (Set via environment variables or replace for local testing)
TWILIO_ACCOUNT_SID = 'YOUR_TWILIO_ACCOUNT_SID'
TWILIO_AUTH_TOKEN = 'YOUR_TWILIO_AUTH_TOKEN'
TWILIO_PHONE_NUMBER = 'YOUR_TWILIO_PHONE_NUMBER'

# Destination Number
EMERGENCY_CONTACT = 'YOUR_EMERGENCY_CONTACT_NUMBER'

# Initialize Twilio Client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/alert', methods=['POST'])
def handle_emergency():
    data = request.json
    print("\n[ALERT] Garmin watch detected anomaly. Triggering Twilio API...")
    
    heart_rate = data.get("heartRate", "Unknown")
    
    # Trigger an automated Voice Call
    try:
        call = client.calls.create(
            twiml=f'<Response><Say voice="alice" loop="2">Emergency alert! Abnormal heart rate of {heart_rate} BPM detected for Roy.</Say></Response>',
            to=EMERGENCY_CONTACT,
            from_=TWILIO_PHONE_NUMBER
        )
        print(f"[SUCCESS] Voice Call initiated! Call SID: {call.sid}")
        return jsonify({"status": "success", "source": "voice_call"}), 200
        
    except Exception as e:
        print(f"[ERROR] Failed to make call: {e}")
        return jsonify({"status": "failed", "error": str(e)}), 500

if __name__ == '__main__':
    # Running on port 5000 to match ngrok tunnel
    app.run(host='0.0.0.0', port=5000, debug=True)
