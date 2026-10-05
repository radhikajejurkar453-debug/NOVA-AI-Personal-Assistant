import random
import time
import webbrowser
from urllib.parse import quote_plus

from Nova_Data.Nova_Dlg_Dataset.dlg import yt_search, s1, s2
from Functions.Nova_Speak.speak import speak


# ============================================================
# YOUTUBE SEARCH
# ============================================================

def youtube_search(text):

    if not text or not text.strip():
        return False

    try:
        # Clean the search text
        text = text.strip()

        # Nova speaks before searching
        speak(random.choice(yt_search))

        # Convert search text into a URL-safe format
        search_query = quote_plus(text)

        # Direct YouTube search URL
        youtube_url = (
            "https://www.youtube.com/results?search_query="
            + search_query
        )

        print("YouTube Search:", text)
        print("Opening:", youtube_url)

        # Open YouTube search directly
        webbrowser.open(youtube_url)

        # Give browser a little time to start
        time.sleep(3)

        # Tell user that search is being performed
        speak(random.choice(s1))

        # Wait a little for YouTube results to load
        time.sleep(2)

        # Search completed
        speak(random.choice(s2))

        return True

    except Exception as e:

        print("YouTube search error:", e)

        return False



# ============================================================
# TESTING
# ============================================================
"""
if __name__ == "__main__":
    youtube_search("Mythpat")
"""