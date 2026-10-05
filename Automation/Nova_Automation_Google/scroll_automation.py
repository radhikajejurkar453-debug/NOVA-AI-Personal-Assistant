import pyautogui as ui


# ============================================================
# CHROME AUTOMATION
# ============================================================

def scroll_up():

    ui.press("pageup")


def scroll_down():

    ui.press("pagedown")


def page_up():

    ui.press("pageup")


def page_down():

    ui.press("pagedown")


def go_to_top():

    ui.hotkey("ctrl", "home")


def go_to_bottom():

    ui.hotkey("ctrl", "end")