import pyautogui as ui

def close_youtube_tab():
    ui.hotkey("ctrl", "w")

def volume_up():
    ui.press("up")


def volume_down():
    ui.press("down")


def seek_backward():
    ui.press("left")


def seek_forward():
    ui.press("right")


def seek_backward_10():
    ui.press("j")


def seek_forward_10():
    ui.press("l")


def previous_frame():
    ui.press(",")


def next_frame():
    ui.press(".")


def seek_percent(percent):

    if percent in range(0, 10):
        ui.press(str(percent))


def beginning():
    ui.press("home")


def end():
    ui.press("end")


def previous_chapter():
    ui.hotkey("ctrl", "left")


def next_chapter():
    ui.hotkey("ctrl", "right")


def speed_down():
    ui.hotkey("shift", ",")


def speed_up():
    ui.hotkey("shift", ".")


def next_video():
    ui.hotkey("shift", "n")


def previous_video():
    ui.hotkey("shift", "p")