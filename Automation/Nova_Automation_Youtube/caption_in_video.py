import time
import pyautogui as ui

def toggle_captions():
    ui.press("c")

def increase_caption_size():
    ui.hotkey("shift", "=")

def decrease_caption_size():
    ui.press("-")

def increase_caption_opacity():
    ui.press("o")

def caption_window_opacity():
    ui.press("w")

def caption_window_opacity_change():
    ui.press("w")

def open_caption_settings():
    ui.press("c")
    time.sleep(0.5)

def close_caption_settings():
    ui.press("esc")

def caption_font_increase():
    ui.hotkey("shift", "=")

def caption_font_decrease():
    ui.press("-")
