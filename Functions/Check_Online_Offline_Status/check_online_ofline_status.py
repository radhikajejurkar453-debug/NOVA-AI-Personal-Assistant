# ============================================================
# NOVA ONLINE / OFFLINE STATUS
# ============================================================

import requests

from Functions.Offline_Voice.speak2 import fspeak
from Functions.Nova_Speak.speak import speak


# ============================================================
# UI NETWORK STATUS
# ============================================================

def ui_network_status(status):

    try:

        from Interface.nova_ui_bridge import emit_network_status

        emit_network_status(
            status
        )

    except Exception:

        pass


# ============================================================
# CHECK INTERNET
# ============================================================

def is_online(
    url="https://www.google.com/generate_204",
    timeout=2
):

    try:

        response = requests.get(
            url,
            timeout=timeout
        )

        return (
            200 <= response.status_code < 400
        )

    except requests.RequestException:

        return False

    except Exception:

        return False


# ============================================================
# GET NETWORK STATUS
# ============================================================

def get_network_status():

    if is_online():

        ui_network_status(
            "ONLINE"
        )

        return True

    else:

        ui_network_status(
            "OFFLINE"
        )

        return False


# ============================================================
# NOVA INTERNET STATUS
# ============================================================

def internet_status():

    if get_network_status():

        return "Yes! I'm online and ready."

    else:

        return (
            "Hey there! I'm Nova. "
            "Sorry, but I am offline right now. "
            "My offline features are still available."
        )


# ============================================================
# TESTING
# ============================================================

"""
if __name__ == "__main__":

    status = internet_status()

    print(status)

    speak(status)
"""
