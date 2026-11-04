import unittest
from unittest.mock import patch
# Import the Flask app instance from your main application file
from app import app  

class EmergencyAlertTests(unittest.TestCase):
    
    def setUp(self):
        """Set up a virtual test client for the Flask application before each test."""
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.client.calls.create')  # Mocks the actual Twilio API call to prevent making real phone calls
    def test_high_heart_rate_triggers_alert(self, mock_twilio_call):
        """An alert from the watch places exactly one call, and the call says the real heart rate."""
        # Simulate an incoming HTTP POST request from the watch with high HR data
        response = self.app.post('/alert', json={'heartRate': 175})

        # Assert that the server responds with a 200 SUCCESS status code
        self.assertEqual(response.status_code, 200)

        # Assert that the Twilio API integration was triggered exactly once
        mock_twilio_call.assert_called_once()

        # Assert that the spoken message contains the heart rate that was sent
        # (this check would have caught the "hr" / "heartRate" key mismatch)
        self.assertIn('175', mock_twilio_call.call_args.kwargs['twiml'])

    @patch('app.client.calls.create')
    def test_server_forwards_every_alert_it_receives(self, mock_twilio_call):
        """The 170 / 40 thresholds are checked on the watch. The server trusts the watch
        and places a call for every alert it receives."""
        response = self.app.post('/alert', json={'heartRate': 75})

        self.assertEqual(response.status_code, 200)
        mock_twilio_call.assert_called_once()

if __name__ == '__main__':
    unittest.main()
