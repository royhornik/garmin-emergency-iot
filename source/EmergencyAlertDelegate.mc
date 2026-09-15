import Toybox.Lang;
import Toybox.WatchUi;

class EmergencyAlertDelegate extends WatchUi.BehaviorDelegate {

    function initialize() {
        BehaviorDelegate.initialize();
    }

    function onMenu() as Boolean {
        WatchUi.pushView(new Rez.Menus.MainMenu(), new EmergencyAlertMenuDelegate(), WatchUi.SLIDE_UP);
        return true;
    }

}