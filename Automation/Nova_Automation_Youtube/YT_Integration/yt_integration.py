import random
import webbrowser
import pyautogui as ui

from Nova_Data.Nova_Dlg_Dataset.dlg import *
from Functions.Nova_Listen.listen import listen
from Functions.Nova_Speak.speak import speak

from Automation.Nova_Automation_Youtube.play_music_in_youtube import (
    play_music_on_youtube
)

from Automation.Nova_Automation_Youtube.play_pause_video_in_youtube import (
    play_pause
)

from Automation.Nova_Automation_Youtube.caption_in_video import *

from Automation.Nova_Automation_Youtube.search_in_youtube import (
    youtube_search
)

from Automation.Nova_Automation_Youtube.manual_search_in_youtube import (
    search_manual
)

from Automation.Nova_Automation_Youtube.another_automation_in_yt import *

from Automation.Nova_Automation_Youtube.youtube_video_playback import *


# ============================================================
# OPEN YOUTUBE WEBSITE
# ============================================================
def open_youtube():

    try:

        # ----------------------------------------------------
        # NOVA SPEAKS
        # ----------------------------------------------------

        speak(
            "Opening YouTube."
        )

        # ----------------------------------------------------
        # OPEN YOUTUBE
        # ----------------------------------------------------

        webbrowser.open(
            "https://www.youtube.com"
        )

        print(
            "[Nova] YouTube opened."
        )

        return True

    except Exception as e:

        print(
            f"[Nova] YouTube opening error: {e}"
        )

        speak(
            "Sorry, I couldn't open YouTube."
        )

        return False
# ============================================================
# CLOSE CURRENT BROWSER TAB
# ============================================================
def close_youtube_tab():

    try:

        speak("Closing YouTube.")

        ui.hotkey("ctrl", "w")

        print("[Nova] YouTube tab closed.")

        return True

    except Exception as e:

        print(f"[Nova] Error closing YouTube tab: {e}")

        speak("Sorry, I couldn't close YouTube.")

        return False

# ============================================================
# YOUTUBE COMMAND
# ============================================================

def youtube_cmd(text):

    if not text:
        return False


    # --------------------------------------------------------
    # CLEAN COMMAND
    # --------------------------------------------------------

    text = text.lower().strip()


    # ========================================================
    # OPEN YOUTUBE
    # ========================================================

    if text in [
        "youtube",
        "open youtube",
        "open youtube website",
        "open youtube site",
        "go to youtube",
        "go to youtube website"
    ]:

        return open_youtube()


    # ========================================================
    # CLOSE YOUTUBE / MUSIC / VIDEO
    # ========================================================

    elif text in [
        "close youtube",
        "close youtube tab",
        "close youtube window",
        "close music",
        "close video"
    ]:

        return close_youtube_tab()


    # ========================================================
    # PLAY MUSIC WITH SONG NAME
    #
    # Example:
    #
    # play touch
    # play sunflower
    # play shape of you
    #
    # ========================================================

    elif text.startswith("play "):

        song = text[
            len("play "):
        ].strip()


        if not song:

            return False


        print(
            f"[Nova] Playing: {song}"
        )


        try:

            play_music_on_youtube(
                song
            )

            return True


        except Exception as e:

            print(
                f"[Nova] Play music error: {e}"
            )

            speak(
                "Sorry, I couldn't play that."
            )

            return False


    # ========================================================
    # PLAY MUSIC WITHOUT SONG NAME
    # ========================================================

    elif text in [
        "play music",
        "play song",
        "play something",
        "play a song"
    ]:

        speak(
            random.choice(q)
        )


        song = listen()


        if not song:

            return False


        try:

            play_music_on_youtube(
                song
            )

            return True


        except Exception as e:

            print(
                f"[Nova] Play music error: {e}"
            )

            speak(
                "Sorry, I couldn't play that."
            )

            return False


    # ========================================================
    # PLAY / PAUSE
    # ========================================================

    elif text in x1:

        play_pause()

        return True


    elif text in x2:

        play_pause()

        return True


    # ========================================================
    # VOLUME UP
    # ========================================================

    elif text in [
        "increase volume",
        "volume up",
        "increase youtube volume"
    ]:

        volume_up()

        return True


    # ========================================================
    # VOLUME DOWN
    # ========================================================

    elif text in [
        "decrease volume",
        "volume down",
        "decrease youtube volume"
    ]:

        volume_down()

        return True


    # ========================================================
    # MUTE / UNMUTE
    # ========================================================

    elif text in [
        "mute",
        "mute youtube",
        "unmute",
        "unmute youtube"
    ]:

        mute_unmute()

        return True


    # ========================================================
    # SEEK FORWARD
    # ========================================================

    elif text in [
        "seek forward",
        "forward",
        "skip forward"
    ]:

        seek_forward()

        return True


    # ========================================================
    # SEEK BACKWARD
    # ========================================================

    elif text in [
        "seek backward",
        "backward",
        "skip backward"
    ]:

        seek_backward()

        return True


    # ========================================================
    # SEEK FORWARD 10 SECONDS
    # ========================================================

    elif text in [
        "seek forward 10 seconds",
        "forward 10 seconds",
        "skip 10 seconds"
    ]:

        seek_forward_10()

        return True


    # ========================================================
    # SEEK BACKWARD 10 SECONDS
    # ========================================================

    elif text in [
        "seek backward 10 seconds",
        "backward 10 seconds",
        "back 10 seconds"
    ]:

        seek_backward_10()

        return True


    # ========================================================
    # FRAME CONTROL
    # ========================================================

    elif text in [
        "seek forward frame",
        "next frame"
    ]:

        next_frame()

        return True


    elif text in [
        "seek backward frame",
        "previous frame"
    ]:

        previous_frame()

        return True


    # ========================================================
    # BEGINNING
    # ========================================================

    elif text in [
        "seek to beginning",
        "go to beginning",
        "go to start"
    ]:

        beginning()

        return True


    # ========================================================
    # END
    # ========================================================

    elif text in [
        "seek to end",
        "go to end"
    ]:

        end()

        return True


    # ========================================================
    # CHAPTER CONTROL
    # ========================================================

    elif text in [
        "previous chapter",
        "go to previous chapter",
        "seek to previous chapter"
    ]:

        previous_chapter()

        return True


    elif text in [
        "next chapter",
        "go to next chapter",
        "seek to next chapter"
    ]:

        next_chapter()

        return True


    # ========================================================
    # PLAYBACK SPEED
    # ========================================================

    elif text in [
        "decrease playback speed",
        "slow down video"
    ]:

        speed_down()

        return True


    elif text in [
        "increase playback speed",
        "speed up video"
    ]:

        speed_up()

        return True


    # ========================================================
    # NEXT / PREVIOUS VIDEO
    # ========================================================

    elif text in [
        "next video",
        "play next video",
        "next song"
    ]:

        next_video()

        return True


    elif text in [
        "previous video",
        "play previous video",
        "previous song"
    ]:

        previous_video()

        return True


    # ========================================================
    # CAPTIONS
    # ========================================================

    elif text in [
        "turn on captions",
        "turn off captions",
        "toggle captions",
        "captions",
        "subtitles"
    ]:

        toggle_captions()

        return True


    # ========================================================
    # CAPTION SIZE
    # ========================================================

    elif text in [
        "increase caption size",
        "increase subtitle size"
    ]:

        increase_caption_size()

        return True


    elif text in [
        "decrease caption size",
        "decrease subtitle size"
    ]:

        decrease_caption_size()

        return True


    # ========================================================
    # FULLSCREEN
    # ========================================================

    elif text in [
        "fullscreen",
        "full screen"
    ]:

        fullscreen()

        return True


    elif text in [
        "exit fullscreen",
        "exit full screen",
        "leave fullscreen"
    ]:

        exit_fullscreen()

        return True


    # ========================================================
    # THEATER MODE
    # ========================================================

    elif text in [
        "theater mode",
        "theatre mode"
    ]:

        theater_mode()

        return True


    # ========================================================
    # MINIPLAYER
    # ========================================================

    elif text in [
        "miniplayer",
        "mini player"
    ]:

        miniplayer()

        return True


    # ========================================================
    # CLOSE DIALOG
    # ========================================================

    elif text in [
        "close dialog",
        "close menu",
        "escape"
    ]:

        close_dialog()

        return True


    # ========================================================
    # 360 VIDEO
    # ========================================================

    elif text in [
        "pan up",
        "look up"
    ]:

        pan_up()

        return True


    elif text in [
        "pan down",
        "look down"
    ]:

        pan_down()

        return True


    elif text in [
        "pan left",
        "look left"
    ]:

        pan_left()

        return True


    elif text in [
        "pan right",
        "look right"
    ]:

        pan_right()

        return True


    elif text in [
        "zoom in",
        "zoom closer"
    ]:

        zoom_in()

        return True


    elif text in [
        "zoom out",
        "zoom away"
    ]:

        zoom_out()

        return True


    # ========================================================
    # OPEN YOUTUBE SEARCH
    # ========================================================

    elif text in [
        "open youtube search",
        "youtube search"
    ]:

        open_search()

        return True


    # ========================================================
    # SEARCH YOUTUBE
    # ========================================================

    elif text.startswith(
        "search youtube "
    ):

        search_text = text.replace(
            "search youtube ",
            "",
            1
        ).strip()


        if search_text:

            return youtube_search(
                search_text
            )

        return False


    # ========================================================
    # SEARCH IN YOUTUBE
    # ========================================================

    elif text.startswith(
        "search in youtube "
    ):

        search_text = text.replace(
            "search in youtube ",
            "",
            1
        ).strip()


        if search_text:

            return youtube_search(
                search_text
            )

        return False


    # ========================================================
    # SEARCH ON YOUTUBE
    # ========================================================

    elif text.startswith(
        "search on youtube "
    ):

        search_text = text.replace(
            "search on youtube ",
            "",
            1
        ).strip()


        if search_text:

            return youtube_search(
                search_text
            )

        return False


    # ========================================================
    # MANUAL SEARCH
    # ========================================================

    elif (
        text.endswith(
            "search in current youtube window"
        )
        or
        text.endswith(
            "search on current youtube window"
        )
        or
        text.endswith(
            "search current youtube window"
        )
    ):

        text = text.replace(
            "search in current youtube window",
            ""
        ).strip()


        text = text.replace(
            "search on current youtube window",
            ""
        ).strip()


        text = text.replace(
            "search current youtube window",
            ""
        ).strip()


        if text:

            return search_manual(
                text
            )

        return False


    # ========================================================
    # SETTINGS
    # ========================================================

    elif text in [
        "settings up",
        "move settings up"
    ]:

        settings_up()

        return True


    elif text in [
        "settings down",
        "move settings down"
    ]:

        settings_down()

        return True


    elif text in [
        "settings left",
        "move settings left"
    ]:

        settings_left()

        return True


    elif text in [
        "settings right",
        "move settings right"
    ]:

        settings_right()

        return True


    elif text in [
        "close settings",
        "close youtube settings"
    ]:

        close_settings()

        return True

    elif text in [
        "scroll up",
        "youtube scroll up",
        "scroll youtube up",
        "move up",
        "page up"
    ]:
        scroll_up()

    elif text in [
        "scroll down",
        "youtube scroll down",
        "scroll youtube down",
        "move down",
        "page down"
    ]:
        scroll_down()

    elif text in [
        "scroll up page",
        "page up youtube",
        "youtube page up"
    ]:
        scroll_up_page()

    elif text in [
        "scroll down page",
        "page down youtube",
        "youtube page down"
    ]:
        scroll_down_page()

    elif text in [
        "next control",
        "move to next control",
        "next tab"
    ]:
        next_control()

    elif text in [
        "previous control",
        "move to previous control",
        "previous tab"
    ]:
        previous_control()

    elif text in [
        "select control",
        "activate control",
        "select"
    ]:
        select_control()

    elif text in [
        "tab next",
        "next tab control"
    ]:
        tab_next()

    elif text in [
        "tab previous",
        "previous tab control"
    ]:
        tab_previous()

    elif text in [
        "press enter",
        "enter"
    ]:
        enter()

    elif text in [
        "press space",
        "space"
    ]:
        space()




    # ========================================================
    # PARTY MODE
    # ========================================================

    elif text in [
        "party mode",
        "awesome mode"
    ]:

        party_mode()

        return True


    # ========================================================
    # REFRESH
    # ========================================================

    elif text in [
        "refresh youtube",
        "refresh"
    ]:

        refresh()

        return True


    # ========================================================
    # NOT A YOUTUBE COMMAND
    # ========================================================

    return False