import random
import time
import webbrowser
from urllib.parse import quote

from Nova_Data.Nova_Dlg_Dataset.dlg import s1, s2
from Functions.Nova_Speak.speak import speak


# ============================================================
# SEARCH YOUTUBE
# ============================================================

def search_manual(text):

    if not text:
        return False

    text = text.strip()

    if not text:
        return False

    # --------------------------------------------------------
    # Speak search message
    # --------------------------------------------------------

    s12 = random.choice(s1)
    speak(s12)

    time.sleep(0.5)

    # --------------------------------------------------------
    # Open YouTube search directly
    # --------------------------------------------------------

    search_url = (
        "https://www.youtube.com/results?search_query="
        + quote(text)
    )

    webbrowser.open(search_url)

    # --------------------------------------------------------
    # Wait for browser
    # --------------------------------------------------------

    time.sleep(3)

    # --------------------------------------------------------
    # Speak completion message
    # --------------------------------------------------------

    s12 = random.choice(s2)
    speak(s12)

    return True



"""
# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    search_manual("Sunflower")
"""
