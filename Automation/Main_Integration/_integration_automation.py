from Automation.Nova_Common_Automation.common_intregration import *
from Automation.Nova_Automation_Google.Google_integration.google_integration import *
from Automation.Nova_Automation_Battery.Battery_Integration.battry_integration import *
from Automation.Nova_Automation_Youtube.YT_Integration.yt_integration import *


def Automation(text):

    if not text:
        return False

    text = text.lower().strip()


    # ========================================================
    # YOUTUBE
    # ========================================================

    if youtube_cmd(text):

        return True


    # ========================================================
    # GOOGLE / WEBSITES
    # ========================================================

    if google_cmd(text):

        return True


    # ========================================================
    # COMMON
    # ========================================================

    if common_cmd(text):

        return True

    # ========================================================
    # Battery
    # ========================================================

    if  battery_cmd(text):

        return True


    return False
