import random
import time
import psutil
import threading

from Nova_Data.Nova_Dlg_Dataset.dlg import *
from Functions.Nova_Speak.speak import *


# ============================================================
# GLOBAL FLAG
# ============================================================

battery_alert_running = False


# ============================================================
# BATTERY ALERT
# ============================================================

def battery_alert():
    """
    Monitor battery level in the background.
    """

    global battery_alert_running

    while battery_alert_running:

        battery = psutil.sensors_battery()

        if battery is None:
            print("Battery not detected.")
            return

        percent = int(battery.percent)

        print("Battery level:", percent, "%")

        if percent < 10:

            speak(random.choice(last_low))

        elif percent < 30:

            speak(random.choice(low_b))


        elif percent == 100:

            speak(random.choice(full_battery))

        else:
            speak(f"The battery level is {percent} percent.")

        # Check again after 60 seconds
        time.sleep(350)


# ============================================================
# START BATTERY ALERT
# ============================================================

def start_battery_alert():
    """
    Start battery alert in background thread.
    """

    global battery_alert_running

    if battery_alert_running:
        return

    battery_alert_running = True

    battery_thread = threading.Thread(
        target=battery_alert,
        daemon=True,
        name="BatteryAlert"
    )

    battery_thread.start()

    print("Battery alert started (background thread)")


# ============================================================
# STOP BATTERY ALERT
# ============================================================

def stop_battery_alert():
    """
    Stop battery alert.
    """

    global battery_alert_running

    battery_alert_running = False

    print("Battery alert stopped")


# ============================================================
# TESTING
# ============================================================
"""
if __name__ == "__main__":

    print("BATTERY ALERT TEST STARTED")

    start_battery_alert()

    print("Battery alert is running...")

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        print("\nStopping battery alert...")

        stop_battery_alert()

        print("BATTERY ALERT TEST FINISHED")
"""