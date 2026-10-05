
import speech_recognition as sr
import threading

from Brain.Activity.welcome_greetings import welcome

from Functions.Nova_Listen.listen import *
from Functions.Nova_Speak.speak import *

from Brain.Main_Brain.brain import *

from Automation.Main_Integration._integration_automation import *

from Functions.Main_Function_integration.function_integration import *

from Nova_Data.Nova_Dlg_Dataset.dlg import *

from Brain.Activity.wish_greetings import *
from Brain.advice import *
from Brain.Activity.joke import *

from Automation.Nova_Automation_Battery.battery_plug_check import *
from Automation.Nova_Automation_Battery.battery_alert import *


# ============================================================
# NOVA STATE
# ============================================================

NOVA_RUNNING = False
NOVA_LOCK = threading.Lock()


# ============================================================
# SPEECH RECOGNIZER
# ============================================================

recognizer = sr.Recognizer()
recognizer.operation_timeout = 5


# ============================================================
# UI BRIDGE HELPERS
# ============================================================

def ui_status(status):

    try:

        from Interface.nova_ui_bridge import emit_status

        emit_status(status)

    except Exception:

        pass


def ui_error(error):

    try:

        from Interface.nova_ui_bridge import emit_error

        emit_error(error)

    except Exception:

        pass


# ============================================================
# FIX NOVA RECOGNITION
# ============================================================

def fix_nova_trigger(text):

    words = text.split()

    if not words:

        return text


    first_word = words[0]


    # --------------------------------------------------------
    # Common speech-recognition mistakes
    # --------------------------------------------------------

    if first_word in [
        "nov",
        "novaa"
    ]:

        words[0] = "nova"


    return " ".join(words)


# ============================================================
# CHECK NOVA TRIGGER
# ============================================================

def has_nova_trigger(text):

    """
    Nova is considered a trigger ONLY when it is
    the first word.

    Valid:

        nova
        nova search python
        nova, search python

    Invalid trigger:

        what is nova
        tell me about nova
        history of nova
    """

    text = text.strip()


    if text == "nova":

        return True


    if text.startswith("nova "):

        return True


    if text.startswith("nova,"):

        return True


    return False


# ============================================================
# REMOVE NOVA TRIGGER
# ============================================================

def remove_nova_trigger(text):

    """
    Removes Nova only when it is being used as the
    trigger at the beginning.

    Examples:

        nova search python
            -> search python

        nova, search python
            -> search python

        nova
            -> ""

        what is nova
            -> unchanged
    """

    text = text.strip()


    # --------------------------------------------------------
    # Nova alone
    # --------------------------------------------------------

    if text == "nova":

        return ""


    # --------------------------------------------------------
    # Nova followed by comma
    # --------------------------------------------------------

    if text.startswith("nova,"):

        return text[5:].strip()


    # --------------------------------------------------------
    # Nova followed by space
    # --------------------------------------------------------

    if text.startswith("nova "):

        return text[5:].strip()


    return text


# ============================================================
# COMMAND MODE
# ============================================================

def co_main():

    while NOVA_RUNNING:

        text = listen(recognizer)


        # ----------------------------------------------------
        # No speech
        # ----------------------------------------------------

        if not text:

            continue


        # ----------------------------------------------------
        # Clean text
        # ----------------------------------------------------

        text = text.lower().strip()


        # ====================================================
        # FIX NOVA RECOGNITION
        # ====================================================

        text = fix_nova_trigger(text)


        print(
            "[NOVA] Heard:",
            text
        )


                # ====================================================
        # CHECK NOVA TRIGGER
        # ====================================================

        nova_triggered = has_nova_trigger(text)


        # ====================================================
        # REMOVE NOVA FROM COMMAND
        # ====================================================

        command_text = remove_nova_trigger(text)


        # ====================================================
        # NOVA ALONE
        # ====================================================

        if nova_triggered and not command_text:

            print(
                "[NOVA] Nova trigger detected."
            )

            ui_status("ACTIVE")

            continue


        # ====================================================
        # SHUTDOWN WITH NOVA
        # ====================================================

        if nova_triggered and command_text in EXIT_COMMANDS:

            speak("Goodbye...")

            print(
                "[NOVA] Shutdown command received."
            )

            ui_status("SHUTDOWN_REQUESTED")

            return False


        # ====================================================
        # AUTOMATION
        # ====================================================

        if Automation(command_text):

            continue


        # ====================================================
        # NORMAL FUNCTION COMMANDS
        # ====================================================

        if function_cmd(command_text):

            continue


        # ====================================================
        # GREETINGS
        # ====================================================

        if Greeting(command_text):

            continue


        # ====================================================
        # JOKE
        # ====================================================

        if "joke" in command_text:

            jokes()

            continue


        # ====================================================
        # ADVICE
        # ====================================================

        if "advice" in command_text:

            advice()

            continue


        # ====================================================
        # NOVA BRAIN
        # ====================================================

        # IMPORTANT:
        #
        # brain_cmd() is called ONLY when Nova was used
        # as the trigger at the beginning.
        #
        # Example:
        #
        # "Nova, search Python"
        #
        # becomes:
        #
        # "search Python"
        #
        # and only this command is sent to brain_cmd().
        #

        if nova_triggered:

            if command_text:

                print(
                    "[NOVA] Executing:",
                    command_text
                )

                brain_cmd(command_text)

            continue


        # ====================================================
        # NO NOVA TRIGGER
        # ====================================================

        # Do NOT send the sentence to brain_cmd().
        #
        # This prevents accidental searches caused by the
        # word "Nova" appearing somewhere inside a sentence.
        #

        print(
            "[NOVA] No Nova trigger detected."
        )


    return False


# ============================================================
# WAKE WORD LOOP
# ============================================================

def main():

    print(
        "[NOVA] Wake-word system started."
    )

    ui_status("SLEEPING")


    while NOVA_RUNNING:

        wake_cmd = hearing()


        # ----------------------------------------------------
        # Backend stopped
        # ----------------------------------------------------

        if not NOVA_RUNNING:

            break


        # ----------------------------------------------------
        # No speech
        # ----------------------------------------------------

        if not wake_cmd:

            continue


        wake_cmd = wake_cmd.lower().strip()


        # ====================================================
        # WAKE WORD DETECTED
        # ====================================================

        if wake_cmd in wake_key_word:

            print(
                "[NOVA] Wake word detected."
            )

            ui_status("ACTIVE")


            # ------------------------------------------------
            # Greeting
            # ------------------------------------------------

            wake_great = welcome()

            speak(wake_great)


            # ------------------------------------------------
            # Enter command mode
            # ------------------------------------------------

            result = co_main()


            # ------------------------------------------------
            # Shutdown requested
            # ------------------------------------------------

            if result is False:

                print(
                    "[NOVA] Returning from command mode."
                )

                break


    print(
        "[NOVA] Main loop stopped."
    )


# ============================================================
# START NOVA
# ============================================================

def nova():

    global NOVA_RUNNING


    # ========================================================
    # PREVENT DUPLICATE NOVA INSTANCE
    # ========================================================

    with NOVA_LOCK:

        if NOVA_RUNNING:

            print(
                "[NOVA] Nova is already running."
            )

            return


        NOVA_RUNNING = True


    print()
    print("================================================")
    print("             NOVA BACKEND STARTED")
    print("================================================")
    print()


    ui_status("STARTING")


    # ========================================================
    # MAIN NOVA THREAD
    # ========================================================

    t1 = threading.Thread(
        target=main,
        name="NovaMain",
        daemon=True
    )


    # ========================================================
    # BATTERY THREAD
    # ========================================================

    t2 = threading.Thread(
        target=battery_alert,
        name="BatteryAlert",
        daemon=True
    )


    # ========================================================
    # CHARGER THREAD
    # ========================================================

    t3 = threading.Thread(
        target=battery_plug_check,
        name="BatteryPlugCheck",
        daemon=True
    )


    try:

        t1.start()

        t2.start()

        t3.start()


        ui_status("SLEEPING")


        # ----------------------------------------------------
        # Keep backend alive while Nova is running
        # ----------------------------------------------------

        t1.join()


    except Exception as e:

        print(
            "[NOVA ERROR]",
            e
        )

        ui_error(str(e))


    finally:

        NOVA_RUNNING = False


        print()
        print("================================================")
        print("             NOVA BACKEND STOPPED")
        print("================================================")
        print()


        ui_status("READY")

"""
# ============================================================
# DIRECT RUN
# ============================================================

if __name__ == "__main__":

    nova()

"""