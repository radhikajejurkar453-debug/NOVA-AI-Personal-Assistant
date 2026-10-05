import random
import time
import psutil
import threading

from Nova_Data.Nova_Dlg_Dataset.dlg import *
from Functions.Nova_Speak.speak import *


# Global flag
battery_monitor_running = True


def battery_plug_check():

    """
    Check charger status when Nova starts
    and continuously monitor for plug-in / plug-out changes.
    """

    global battery_monitor_running

    battery = psutil.sensors_battery()

    if battery is None:
        print("[Nova Battery] Battery information unavailable.")
        return

    # ============================================================
    # CHECK CURRENT CHARGER STATUS
    # ============================================================

    previous_state = battery.power_plugged

    if previous_state:

        print("[Nova Battery] Charger is connected.")

        speak(
            random.choice(plug_in)
        )

    else:

        print("[Nova Battery] Charger is not connected.")

        speak(
            random.choice(plug_out)
        )

    # ============================================================
    # CONTINUOUS MONITORING
    # ============================================================

    while battery_monitor_running:

        time.sleep(2)

        battery = psutil.sensors_battery()

        if battery is None:
            return

        current_state = battery.power_plugged

        # ========================================================
        # CHARGER STATE CHANGED
        # ========================================================

        if current_state != previous_state:

            if current_state:

                print("[Nova Battery] Charger connected.")

                speak(
                    random.choice(plug_in)
                )

            else:

                print("[Nova Battery] Charger disconnected.")

                speak(
                    random.choice(plug_out)
                )

            previous_state = current_state


def start_battery_monitor():

    """
    Start battery monitoring in background thread.
    """

    global battery_monitor_running

    if battery_monitor_running:
        return

    battery_monitor_running = True

    battery_thread = threading.Thread(
        target=battery_plug_check,
        daemon=True,
        name="BatteryMonitor"
    )

    battery_thread.start()

    print("Battery monitor started.")


def stop_battery_monitor():

    """
    Stop battery monitoring gracefully.
    """

    global battery_monitor_running

    battery_monitor_running = False

    print("Battery monitor stopped.")