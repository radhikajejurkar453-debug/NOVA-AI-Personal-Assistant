# ============================================================
# GOOGLE SEARCH FUNCTION
# ============================================================

import random
import time

from Nova_Data.Nova_Dlg_Dataset.dlg import *
from Functions.Nova_Speak.speak import *


# ============================================================
# GOOGLE SEARCH FUNCTION
# ============================================================

def search_google(text):
    """
    Search Google for a query and speak confirmation.
    Uses pywhatkit to perform the search.
    """

    if not text or not text.strip():
        return False

    try:

        # ----------------------------------------------------
        # Import pywhatkit only when Google search is requested
        # ----------------------------------------------------

        import pywhatkit


        # ----------------------------------------------------
        # Speak search confirmation
        # ----------------------------------------------------

        speak(
            random.choice(s1)
        )


        # ----------------------------------------------------
        # Perform Google search using pywhatkit
        # ----------------------------------------------------

        pywhatkit.search(
            text
        )


        # ----------------------------------------------------
        # Wait for Google search to open
        # ----------------------------------------------------

        time.sleep(2)


        # ----------------------------------------------------
        # Speak result dialogue
        # ----------------------------------------------------

        speak(
            random.choice(s2)
        )


        return True


    except Exception as e:

        print(
            f"[ERROR] Google search error: {e}"
        )


        speak(
            "Search failed. Please try again."
        )


        return False


# ============================================================
# TEST
# Remove this after testing
# ============================================================

"""
if __name__ == "__main__":

    search_google(
        "spider man"
    )
"""