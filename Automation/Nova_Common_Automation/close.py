import random
import pyautogui as ui

from Nova_Data.Nova_Dlg_Dataset.dlg import close_dlg
from Functions.Nova_Speak.speak import *


# ============================================================
# CLOSE WINDOW
# ============================================================

def close_window():

    if not close_dlg:

        speak(
            "Closing window."
        )

    else:

        speak(
            random.choice(close_dlg)
        )

    # --------------------------------------------------------
    # Close active window
    # --------------------------------------------------------

    ui.hotkey(
        "alt",
        "F4"
    )

    return True


# ============================================================
# CLOSE TAB
# ============================================================

def close_tab():

    speak(
        "Closing tab."
    )

    # --------------------------------------------------------
    # Close active browser tab
    # --------------------------------------------------------

    ui.hotkey(
        "ctrl",
        "w"
    )

    return True