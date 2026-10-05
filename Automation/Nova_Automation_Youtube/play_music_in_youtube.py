import random
import time

from Nova_Data.Nova_Dlg_Dataset.dlg import playsong, playing_dlg
from Functions.Nova_Speak.speak import speak


def play_music_on_youtube(text):

    try:

        # ----------------------------------------------------
        # Import pywhatkit only when YouTube is actually used
        # ----------------------------------------------------

        import pywhatkit as kt

        speak(
            random.choice(
                playsong
            )
        )

        kt.playonyt(
            text
        )

        time.sleep(
            3
        )

        speak(
            random.choice(
                playing_dlg
            )
        )

        return True

    except Exception as e:

        print(
            "[NOVA] YouTube music error:",
            e
        )

        speak(
            "Sorry, I could not open YouTube."
        )

        return False


# ============================================================
# TESTING
# ============================================================
"""
if __name__ == "__main__":
    play_music_on_youtube("Touch")
"""