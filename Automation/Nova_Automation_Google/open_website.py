import difflib
import random
import re
import webbrowser

from urllib.parse import urlparse

from Nova_Data.Nova_Dlg_Dataset.dlg import (
    open_maybe,
    open_dlg,
    sorry_open,
    success_open,
    websites
)

from Functions.Nova_Speak.speak import speak


# ============================================================
# OPEN WEBSITE URL
# ============================================================

def open_url(url):

    try:
        webbrowser.open_new_tab(url)
        return True

    except Exception as e:
        print(f"[Nova] Website opening error: {e}")
        return False


# ============================================================
# NORMALIZE WEBSITE INPUT
# ============================================================

def normalize_website_name(text):

    website_name = text.lower().strip()

    # Remove the command prefix.
    website_name = re.sub(
        r"^(open|launch|visit|go to)\s+",
        "",
        website_name,
        count=1
    ).strip()

    # Remove optional prefixes.
    website_name = re.sub(
        r"^(the\s+)?(website|site)\s+",
        "",
        website_name,
        count=1
    ).strip()

    # Remove common trailing words.
    website_name = re.sub(
        r"\s+(website|site|webpage)$",
        "",
        website_name
    ).strip()

    return website_name


# ============================================================
# BUILD DIRECT WEBSITE URL
# ============================================================

def build_website_url(website_name):

    website_name = website_name.strip()

    if not website_name:
        return None

    # If the user supplied a full URL, preserve its domain.
    if website_name.startswith(
        ("https://", "http://")
    ):
        candidate = website_name

    else:
        # Remove spaces from spoken domains:
        # "dash dot com" -> "dash.com"
        # "example dot org" -> "example.org"
        candidate = website_name

        candidate = re.sub(
            r"\s+dot\s+",
            ".",
            candidate
        )

        # "www example com" -> "www.example.com"
        candidate = re.sub(
            r"^www\s+",
            "www.",
            candidate
        )

        # Remove spaces around dots.
        candidate = re.sub(
            r"\s*\.\s*",
            ".",
            candidate
        )

        # Convert a simple domain into an HTTPS URL.
        if "." not in candidate:
            candidate = candidate + ".com"

        candidate = "https://" + candidate

    # Validate the URL before opening it.
    try:
        parsed = urlparse(candidate)

        if (
            parsed.scheme not in ("http", "https")
            or not parsed.hostname
            or "." not in parsed.hostname
        ):
            return None

        # Avoid malformed domains containing spaces.
        if " " in parsed.hostname:
            return None

        return candidate

    except Exception:
        return None


# ============================================================
# OPEN WEBSITE
# ============================================================

def openweb(text):

    if not text:
        return False

    website_name = normalize_website_name(text)

    if not website_name:
        speak("Please tell me which website to open.")
        return False

    print(f"[Nova] Requested website: {website_name}")

    # ========================================================
    # 1. EXACT MATCH FROM YOUR WEBSITE DATASET
    # ========================================================

    if website_name in websites:

        url = websites[website_name]

        print(f"[Nova] Opening saved website: {website_name}")
        print(f"[Nova] URL: {url}")

        speak(
            random.choice(open_dlg) +
            website_name
        )

        if open_url(url):
            speak(random.choice(success_open))
            return True

        speak("Sorry, I couldn't open the website.")
        return False

    # ========================================================
    # 2. DIRECT DOMAIN INPUT
    # ========================================================
    # If the user says a domain such as dashdot.com,
    # chrome.com, or example.org, open that domain directly.
    #
    # Do this BEFORE fuzzy matching to avoid opening an
    # unrelated website with a similar name.
    # ========================================================

    direct_url = build_website_url(website_name)

    looks_like_domain = (
        "." in website_name
        or " dot " in website_name
        or website_name.startswith("www ")
    )

    if direct_url and looks_like_domain:

        print(f"[Nova] Opening direct website: {direct_url}")

        speak(
            random.choice(open_dlg) +
            website_name
        )

        if open_url(direct_url):
            speak(random.choice(success_open))
            return True

        speak("Sorry, I couldn't open that website.")
        return False

    # ========================================================
    # 3. FUZZY MATCH FOR KNOWN WEBSITE NAMES
    # ========================================================
    # Only use fuzzy matching for names without a domain.
    # This helps recognize saved names like YouTube while
    # avoiding wrong matches for explicitly spoken domains.
    # ========================================================

    matches = difflib.get_close_matches(
        website_name,
        websites.keys(),
        n=1,
        cutoff=0.70
    )

    if matches:

        closest_match = matches[0]
        url = websites[closest_match]

        print(f"[Nova] Closest saved website: {closest_match}")
        print(f"[Nova] URL: {url}")

        speak(
            random.choice(open_maybe) +
            random.choice(open_dlg) +
            closest_match
        )

        if open_url(url):
            speak(random.choice(success_open))
            return True

        speak("Sorry, I couldn't open the website.")
        return False

    # ========================================================
    # 4. UNKNOWN NAME: ASK BEFORE GUESSING
    # ========================================================
    # Do not silently open an unrelated website.
    # Ask the user to say the domain, for example:
    # "dashdot.com" or "dash dot com".
    # ========================================================

    print(f"[Nova] Website not found in saved list: {website_name}")

    speak(
        f"I couldn't identify {website_name}. "
        "Please say its website address, such as dash dot com."
    )

    return False


