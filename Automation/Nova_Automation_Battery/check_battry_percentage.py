import psutil
from Functions.Nova_Speak.speak import *

def check_battery_percentage():
    battery = psutil.sensors_battery()
    if battery is None:
        speak("I cannot detect the device battery")
        return
    percent = int(battery.percent)
    speak(
        f"The device is running on {percent}% battery power"
    )
# ============================================================
# TESTING
# ============================================================
"""
if __name__ == "__main__":
    check_battery_percentage()
"""