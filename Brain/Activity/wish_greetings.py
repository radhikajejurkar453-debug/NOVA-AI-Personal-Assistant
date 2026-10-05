from datetime import datetime
import random

from Nova_Data.Nova_Dlg_Dataset.dlg import (
    good_morningdlg,
    good_afternoondlg,
    good_eveningdlg,
    good_nightdlg
)

from Functions.Nova_Speak.speak import speak


def wish():

    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        greeting = random.choice(good_morningdlg)

    elif 12 <= current_hour < 17:
        greeting = random.choice(good_afternoondlg)

    elif 17 <= current_hour < 21:
        greeting = random.choice(good_eveningdlg)

    else:
        greeting = random.choice(good_nightdlg)

    speak(greeting)

    return True


def Greeting(text):

    text = text.lower().strip()

    if (
        "good morning" in text
        or "good afternoon" in text
        or "good evening" in text
        or "good night" in text
    ):
        return wish()

    return False