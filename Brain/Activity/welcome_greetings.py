import random

from Nova_Data.Nova_Dlg_Dataset.dlg import welcomedlg
from Functions.Nova_Speak.speak import speak


def welcome():
    welcome_text = random.choice(welcomedlg)
    speak(welcome_text)
""" 
welcome()
"""
