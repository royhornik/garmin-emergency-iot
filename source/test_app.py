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
        """Test that an abnormally high heart rate triggers the emergency logic and returns 200 OK."""
        # Simulate an incoming HTTP POST request from the watch with high HR data
        response = self.app.post('/alert', json={'heartRate': 175})
        
        # Assert that the server responds with a 200 SUCCESS status code
        self.assertEqual(response.status_code, 200)
        
        # Assert that the Twilio API integration was triggered exactly once
        mock_twilio_call.assert_called_once()

    @patch('app.client.calls.create')
    def test_normal_heart_rate_does_not_trigger_alert(self, mock_twilio_call):
        """Test that a normal heart rate does not trigger any outbound VoIP/telephony alerts."""
        # Simulate an incoming HTTP POST request with safe, baseline HR data
        response = self.app.post('/alert', json={'heartRate': 75})
        
        # Assert that the server processes the request successfully with a 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Assert that the Twilio outbound call was NOT invoked
        mock_twilio_call.assert_not_called()

if __name__ == '__main__':
    unittest.main()