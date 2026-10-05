from Automation.Nova_Common_Automation.open import open
from Automation.Nova_Common_Automation.close import close_window, close_tab

from Nova_Data.Nova_Dlg_Dataset.dlg import websites


# ============================================================
# CURRENTLY OPENED WEBSITE
# ============================================================

current_website = None


# ============================================================
# COMMON COMMAND INTEGRATION
# ============================================================

def common_cmd(text):

    global current_website

    if not text:
        return False

    text = text.lower().strip()


    # ========================================================
    # OPEN WEBSITE / APPLICATION
    # ========================================================

    if text.startswith("open "):

        item = text[len("open "):].strip()

        if not item:
            return False


        # ----------------------------------------------------
        # WEBSITE
        # ----------------------------------------------------

        if item in websites:

            current_website = item

            # Handled by google_cmd/openweb()
            return False


        # ----------------------------------------------------
        # YOUTUBE
        # ----------------------------------------------------

        if item in [
            "youtube",
            "youtube website",
            "youtube site"
        ]:

            current_website = "youtube"

            # Handled by youtube_cmd()
            return False


        # ----------------------------------------------------
        # APPLICATION
        # ----------------------------------------------------

        return open(item)


    # ========================================================
    # CLOSE WINDOW
    # ========================================================

    if text in [
        "close window",
        "close the window"
    ]:

        current_website = None

        return close_window()


    # ========================================================
    # CLOSE TAB
    # ========================================================

    if text in [
        "close tab",
        "close the tab",
        "close current tab",
        "close the current tab"
    ]:

        current_website = None

        return close_tab()


    # ========================================================
    # CLOSE SPECIFIC WEBSITE
    #
    # Example:
    # close instagram
    # close youtube
    # close whatsapp
    # ========================================================

    if text.startswith("close "):

        item = text[len("close "):].strip()


        # ----------------------------------------------------
        # SPECIFIC WEBSITE
        # ----------------------------------------------------

        if item in websites or item == "youtube":

            if current_website == item:

                current_website = None

                return close_tab()


            print(
                f"[Nova] {item} is not the current active tab."
            )

            return False


        # ----------------------------------------------------
        # UNKNOWN CLOSE COMMAND
        # ----------------------------------------------------

        return False


    # ========================================================
    # SIMPLE CLOSE
    # ========================================================

    if text in [
        "close",
        "band kar",
        "band karo"
    ]:

        current_website = None

        return close_window()


    return False