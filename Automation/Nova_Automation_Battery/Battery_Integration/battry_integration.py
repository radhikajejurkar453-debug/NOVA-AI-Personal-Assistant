from Automation.Nova_Automation_Battery.battery_alert import *
from Automation.Nova_Automation_Battery.battery_plug_check import *
from Automation.Nova_Automation_Battery.check_battry_percentage import *

def battery_cmd(text):

    if not text:
        return False

    text = text.lower().strip()

    if "check battery percentage" in text:
        check_battery_percentage()
        return True

    elif "battery alert" in text:
        start_battery_alert()
        return True

    elif "check battery plug" in text:
        start_battery_monitor()
        return True

    return False

# Testing ------------------------
"""
if __name__ == "__main__":
    battery_cmd("check battery percentage")
"""