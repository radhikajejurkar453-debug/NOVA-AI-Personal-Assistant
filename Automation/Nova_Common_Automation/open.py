import time
import random
import pyautogui as ui

from Nova_Data.Nova_Dlg_Dataset.dlg import open_dlg
from Functions.Nova_Speak.speak import speak


# ============================================================
# COMMON APPLICATION OPEN AUTOMATION
# ============================================================

def open(text):

    if not text:
        return False

    text = text.lower().strip()


    # --------------------------------------------------------
    # REMOVE "OPEN"
    # --------------------------------------------------------

    if text.startswith("open "):

        text = text[
            len("open "):
        ].strip()


    if not text:
        return False


    # --------------------------------------------------------
    # NOVA SPEAKS
    # --------------------------------------------------------

    if open_dlg:

        x = random.choice(
            open_dlg
        )

        speak(
            x + text
        )

        time.sleep(0.3)


    # --------------------------------------------------------
    # OPEN APPLICATION
    # --------------------------------------------------------

    ui.press("win")

    time.sleep(0.2)

    ui.write(text)

    time.sleep(0.5)

    ui.press("enter")

    return True