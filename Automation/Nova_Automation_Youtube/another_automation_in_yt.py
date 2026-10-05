import time
import pyautogui as ui


# ============================================================
# SPHERICAL / 360° VIDEO CONTROLS
# ============================================================

def pan_up():
    ui.press("w")


def pan_down():
    ui.press("s")


def pan_left():
    ui.press("a")


def pan_right():
    ui.press("d")


def zoom_in():
    ui.press("]")


def zoom_out():
    ui.press("[")


# ============================================================
# VIDEO CONTROLS
# ============================================================

def open_search():
    ui.press("/")


def mute_unmute():
    ui.press("m")


def fullscreen():
    ui.press("f")

def exit_fullscreen():
    ui.press("esc")

def theater_mode():
    ui.press("t")


def miniplayer():
    ui.press("i")

def close_dialog():
    ui.press("esc")


# ============================================================
# GENERAL CONTROLS
# ============================================================

def next_control():
    ui.press("tab")


def previous_control():
    ui.hotkey("shift", "tab")


def select_control():
    ui.press("enter")

def tab_next():
    ui.press("tab")


def tab_previous():
    ui.hotkey("shift", "tab")


def enter():
    ui.press("enter")


def space():
    ui.press("space")


def refresh():
    ui.hotkey("ctrl", "r")


def close_window():
    ui.hotkey("alt", "f4")

def party_mode():
    ui.write("awesome")

def settings_up():
    ui.press("up")


def settings_down():
    ui.press("down")


def settings_left():
    ui.press("left")


def settings_right():
    ui.press("right")


def close_settings():
    ui.press("esc")


import pyautogui as ui
import time


# =========================================================
# YOUTUBE SCROLL CONTROLS
# =========================================================

def scroll_up():
    ui.scroll(5)


def scroll_down():
    ui.scroll(-5)


def scroll_up_page():
    ui.press("pageup")


def scroll_down_page():
    ui.press("pagedown")


# =========================================================
# YOUTUBE KEYBOARD CONTROLS
# =========================================================

def next_control():
    ui.press("tab")


def previous_control():
    ui.hotkey("shift", "tab")


def select_control():
    ui.press("enter")


def tab_next():
    ui.press("tab")


def tab_previous():
    ui.hotkey("shift", "tab")


def enter():
    ui.press("enter")


def space():
    ui.press("space")


# =========================================================
# YOUTUBE REFRESH
# =========================================================

def refresh():
    ui.hotkey("ctrl", "r")
    time.sleep(2)