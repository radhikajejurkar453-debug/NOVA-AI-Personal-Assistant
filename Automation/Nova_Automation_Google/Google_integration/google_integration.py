from Automation.Nova_Automation_Google.open_website import openweb
from Automation.Nova_Automation_Google.scroll_automation import *
from Automation.Nova_Automation_Google.search_in_google import *
from Automation.Nova_Automation_Google.tab_automation import *

from Nova_Data.Nova_Dlg_Dataset.dlg import websites


# ============================================================
# GOOGLE / CHROME AUTOMATION INTEGRATION
# ============================================================

def google_cmd(text):

    if not text:
        return False

    text = text.lower().strip()


    # ========================================================
    # TAB AUTOMATION
    # ========================================================

    # --------------------------------------------------------
    # OPEN NEW TAB
    # --------------------------------------------------------

    if text in [
        "open new tab",
        "open a new tab",
        "new tab",
        "open tab"
    ]:

        Open_new_tab()

        return True


    # --------------------------------------------------------
    # CLOSE TAB
    # --------------------------------------------------------

    if text in [
        "close tab",
        "close current tab",
        "close this tab"
    ]:

        close_tab()

        return True


    # --------------------------------------------------------
    # REOPEN CLOSED TAB
    # --------------------------------------------------------

    if text in [
        "reopen closed tab",
        "restore closed tab"
    ]:

        reopen_closed_tab()

        return True


    # --------------------------------------------------------
    # NEXT TAB
    # --------------------------------------------------------

    if text in [
        "next tab",
        "move to next tab"
    ]:

        next_tab()

        return True


    # --------------------------------------------------------
    # PREVIOUS TAB
    # --------------------------------------------------------

    if text in [
        "previous tab",
        "move to previous tab"
    ]:

        previous_tab()

        return True


    # --------------------------------------------------------
    # FIRST TAB
    # --------------------------------------------------------

    if text in [
        "first tab",
        "go to first tab"
    ]:

        first_tab()

        return True


    # --------------------------------------------------------
    # SECOND TAB
    # --------------------------------------------------------

    if text in [
        "second tab",
        "go to second tab"
    ]:

        second_tab()

        return True


    # --------------------------------------------------------
    # THIRD TAB
    # --------------------------------------------------------

    if text in [
        "third tab",
        "go to third tab"
    ]:

        third_tab()

        return True


    # ========================================================
    # GOOGLE SEARCH
    # ========================================================

    if text.startswith("search in google "):

        search_text = text[
            len("search in google "):
        ].strip()

        if not search_text:
            return False

        print(
            f"[Nova] Searching Google: {search_text}"
        )

        return search_google(search_text)


    if text.startswith("search on google "):

        search_text = text[
            len("search on google "):
        ].strip()

        if not search_text:
            return False

        print(
            f"[Nova] Searching Google: {search_text}"
        )

        return search_google(search_text)


    if text.startswith("search about "):

        search_text = text[
            len("search about "):
        ].strip()

        if not search_text:
            return False

        print(
            f"[Nova] Searching Google: {search_text}"
        )

        return search_google(search_text)


    # ========================================================
    # OPEN WEBSITE
    # ========================================================

    if text.startswith("open website "):

        website = text[
            len("open website "):
        ].strip()

        if website:

            return openweb(website)

        return False


    if text.startswith("open site "):

        website = text[
            len("open site "):
        ].strip()

        if website:

            return openweb(website)

        return False


    # ========================================================
    # OPEN KNOWN WEBSITE
    # ========================================================

    if text.startswith("open "):

        website = text[
            len("open "):
        ].strip()

        if not website:
            return False

        # ----------------------------------------------------
        # ONLY HANDLE KNOWN WEBSITES
        # ----------------------------------------------------

        if website in websites:

            return openweb(website)

        # ----------------------------------------------------
        # LET OTHER INTEGRATIONS HANDLE IT
        # ----------------------------------------------------

        return False


    # ========================================================
    # SCROLL
    # ========================================================

    if text in [
        "scroll up",
        "scroll upward"
    ]:

        scroll_up()

        return True


    if text in [
        "scroll down",
        "scroll downward"
    ]:

        scroll_down()

        return True


    if text in [
        "page up",
        "page upward",
        "up p"
    ]:

        page_up()

        return True


    if text in [
        "page down",
        "page downward",
        "down p "
    ]:

        page_down()

        return True


    if text in [
        "go to top",
        "go to the top"
    ]:

        go_to_top()

        return True


    if text in [
        "go to bottom",
        "go to the bottom"
    ]:

        go_to_bottom()

        return True


    # ========================================================
    # PAGE AUTOMATION
    # ========================================================

    if text in [
        "hard refresh",
        "hard refresh page"
    ]:

        hard_refresh()

        return True


    if text in [
        "refresh page",
        "refresh"
    ]:

        refresh_page()

        return True


    if text in [
        "go back",
        "back"
    ]:

        go_back()

        return True


    if text in [
        "go forward",
        "forward"
    ]:

        go_forward()

        return True


    # ========================================================
    # CHROME TOOLS
    # ========================================================

    if text in [
        "history",
        "show history"
    ]:

        open_history()

        return True


    if text in [
        " downloads",
        "show downloads"
    ]:

        open_downloads()

        return True


    if text in [
        "bookmarks",
        "show bookmarks",
        "show bookmark"
    ]:

        open_bookmarks()

        return True


    if text in [
        "focus address bar",
        "open address bar"
    ]:

        focus_address_bar()

        return True


    # ========================================================
    # ZOOM
    # ========================================================

    if text in [
        "zoom in",
        "increase zoom"
    ]:

        zoom_in()

        return True


    if text in [
        "zoom out",
        "decrease zoom"
    ]:

        zoom_out()

        return True


    if text in [
        "reset zoom",
        "reset browser zoom"
    ]:

        reset_zoom()

        return True


    # ========================================================
    # BROWSER MENU
    # ========================================================

    if text in [
        "show chrome menu",
        "chrome menu",
        "open browser menu",
        "browser menu"
    ]:
        open_browser_menu()
        return True

    if text in [
        "show dev tools",
        "op developer tools"
    ]:

        open_dev_tools()

        return True


    # ========================================================
    # FULLSCREEN / PRIVATE WINDOW
    # ========================================================

    if text in [
        "toggle full screen",
        "toggle fullscreen",
        "fullscreen"
    ]:

        toggle_full_screen()

        return True


    if text in [
        "show private window",
        "open incognito window",
        "show incognito window"
    ]:

        open_private_window()

        return True


    if text in [
        "close browser",
        "close chrome",
        "close the window"
    ]:

        close_browser()

        return True


    # ========================================================
    # NOT A GOOGLE / CHROME COMMAND
    # ========================================================

    return False