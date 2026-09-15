import Toybox.WatchUi;
import Toybox.Sensor;
import Toybox.Attention;
import Toybox.System;
import Toybox.Graphics;
import Toybox.Lang;
import Toybox.Communications;

// Global test configuration flag. Set to false when deploying to a real device.
const IS_TEST_MODE = false;

class EmergencyAlertView extends WatchUi.View {

    private var mLastHeartRate as Lang.Number = 0;
    
    // Flag to prevent spamming multiple calls. 
    // True means an alert was already triggered and we are currently handling it.
    private var mAlertActive as Lang.Boolean = false;

    function initialize() {
        View.initialize();
    }

    function onShow() as Void {
        Sensor.setEnabledSensors([Sensor.SENSOR_HEARTRATE] as Lang.Array<Sensor.SensorType>);
        Sensor.enableSensorEvents(method(:onSensorUpdate) as Method(info as Sensor.Info) as Void);
    }

    function onSensorUpdate(sensorInfo as Sensor.Info) as Void {
        var heartRate = sensorInfo.heartRate;
        
        // Integration Test Hook: Inject mock data if testing
        if (IS_TEST_MODE && (heartRate == null || heartRate < 100)) {
            //heartRate = 175; 
        }
        
        if (heartRate != null) {
            mLastHeartRate = heartRate;
            //heartRate = 175;
            System.println("Current HR: " + heartRate);
            
            if (heartRate > 170 || heartRate < 40) {
                if (!mAlertActive) {
                    mAlertActive = true;
                    System.println("Critical threshold breached! Triggering emergency alert...");
                    triggerEmergency(heartRate); 
                }
            } else {
                if (mAlertActive) {
                    System.println("Heart rate stabilized. Resetting device alert state.");
                    mAlertActive = false;
                }
            }
        }
    }

    function triggerEmergency(heartRate as Lang.Number) as Void {
        // Trigger local hardware feedback (Vibration and Beep)
        if (Toybox has :Attention) {
            var vibeProfile = [new Attention.VibeProfile(100, 1000)] as Lang.Array<Attention.VibeProfile>;
            Attention.vibrate(vibeProfile);
            Attention.playTone(Attention.TONE_LOUD_BEEP);
        }

        // Dispatch the network call
        makeEmergencyCall(heartRate);
    }

    function makeEmergencyCall(heartRate as Lang.Number) as Void {
        // WARNING: Replace this URL with your current active ngrok forwarding address if it changed
        var url = "https://stir-nape-acorn.ngrok-free.dev/alert"; 
        
        var params = {
            "heartRate" => heartRate
        };
        
        var options = {
            :method => Communications.HTTP_REQUEST_METHOD_POST,
            :headers => {
                "Content-Type" => Communications.REQUEST_CONTENT_TYPE_JSON
            },
            :responseType => Communications.HTTP_RESPONSE_CONTENT_TYPE_JSON
        };
        
        // Make the asynchronous network call and route the response to our callback
        Communications.makeWebRequest(
            url, 
            params, 
            options, 
            method(:onWebResponse) as Method(responseCode as Lang.Number, data as Null or Lang.Dictionary or Lang.String) as Void
        );
    }

    function onWebResponse(responseCode as Lang.Number, data as Null or Lang.Dictionary or Lang.String) as Void {
        System.println("Network Response Code: " + responseCode);
        if (responseCode == 200) {
            System.println("Backend received the alert successfully!");
        } else {
            System.println("Failed to send alert to backend. Error code: " + responseCode);
            // If the network call failed, unlock the alert so it can try again on next reading
            mAlertActive = false; 
        }
    }

    function onUpdate(dc as Graphics.Dc) as Void {
        dc.setColor(Graphics.COLOR_WHITE, Graphics.COLOR_BLACK);
        dc.clear();
        dc.drawText(
            dc.getWidth() / 2, 
            dc.getHeight() / 2, 
            Graphics.FONT_MEDIUM, 
            "Monitoring HR...", 
            Graphics.TEXT_JUSTIFY_CENTER
        );
    }

    function onHide() as Void {
        Sensor.enableSensorEvents(null);
    }
}
