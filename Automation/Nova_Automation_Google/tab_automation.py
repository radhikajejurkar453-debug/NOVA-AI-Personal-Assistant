import time
import pyautogui as ui


# ============================================================
# CHROME / TAB AUTOMATION
# ============================================================

def Open_new_tab():
    ui.hotkey("ctrl", "t")
    time.sleep(0.2)


def close_tab():
    ui.hotkey("ctrl", "w")
    time.sleep(0.2)


def reopen_closed_tab():
    ui.hotkey("ctrl", "shift", "t")
    time.sleep(0.2)


def next_tab():
    ui.hotkey("ctrl", "tab")
    time.sleep(0.2)


def previous_tab():
    ui.hotkey("ctrl", "shift", "tab")
    time.sleep(0.2)


def first_tab():
    ui.hotkey("ctrl", "1")
    time.sleep(0.2)


def second_tab():
    ui.hotkey("ctrl", "2")
    time.sleep(0.2)


def third_tab():
    ui.hotkey("ctrl", "3")
    time.sleep(0.2)


# ============================================================
# PAGE AUTOMATION
# ============================================================

def refresh_page():
    ui.press("f5")
    time.sleep(0.3)


def hard_refresh():
    ui.hotkey("ctrl", "shift", "r")
    time.sleep(0.3)


def go_back():
    ui.hotkey("alt", "left")
    time.sleep(0.3)


def go_forward():
    ui.hotkey("alt", "right")
    time.sleep(0.3)


# ============================================================
# CHROME TOOLS
# ============================================================

def open_history():
    ui.hotkey("ctrl", "h")
    time.sleep(0.3)


def open_downloads():
    ui.hotkey("ctrl", "j")
    time.sleep(0.3)


def open_bookmarks():
    ui.hotkey("ctrl", "shift", "o")
    time.sleep(0.3)


def focus_address_bar():
    ui.hotkey("ctrl", "l")
    time.sleep(0.2)


# ============================================================
# ZOOM
# ============================================================

def zoom_in():
    # Ctrl + = is the reliable keyboard shortcut for Chrome zoom in
    ui.keyDown("ctrl")
    ui.press("=")
    ui.keyUp("ctrl")
    time.sleep(0.3)


def zoom_out():
    ui.keyDown("ctrl")
    ui.press("-")
    ui.keyUp("ctrl")
    time.sleep(0.3)


def reset_zoom():
    ui.hotkey("ctrl", "0")
    time.sleep(0.3)


# ============================================================
# BROWSER MENU / DEV TOOLS
# ============================================================

def open_browser_menu():
    ui.hotkey("alt", "f")
    time.sleep(0.3)


def open_dev_tools():
    ui.press("f12")
    time.sleep(0.3)


# ============================================================
# FULL SCREEN / PRIVATE WINDOW
# ============================================================

def toggle_full_screen():
    ui.press("f11")
    time.sleep(0.3)


def open_private_window():
    ui.hotkey("ctrl", "shift", "n")
    time.sleep(0.3)


# ============================================================
# CLOSE BROWSER
# ============================================================

def close_browser():
    ui.hotkey("alt", "f4")
    time.sleep(0.3)