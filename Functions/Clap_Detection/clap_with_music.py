
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import warnings
warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API"
)

import pygame
import random
import time

from pygame import mixer

from Functions.Clap_Detection.clap_d import (
    TapTester,
    calibrate_microphone,
    REQUIRED_CLAPS
)


# ============================================================
# PLAY RANDOM MUSIC
# ============================================================

def play_random_music(folder_path):

    music_files = [
        file
        for file in os.listdir(folder_path)
        if file.lower().endswith(
            (".mp3", ".wav", ".ogg", ".flac")
        )
    ]

    if not music_files:

        print(
            "No music files found in the music folder."
        )

        return

    selected_music = random.choice(
        music_files
    )

    music_path = os.path.join(
        folder_path,
        selected_music
    )

    try:

        pygame.init()
        mixer.init()


        print("---------------------------------------------------------------------------------------------------------")

        print(
            f"Playing: {selected_music}"
        )

        print("---------------------------------------------------------------------------------------------------------")

        mixer.music.load(
            music_path
        )

        mixer.music.play()

        while mixer.music.get_busy():

            pygame.time.Clock().tick(10)

        mixer.music.stop()
        mixer.quit()

    except Exception as e:

        print(
            f"Error playing music: {e}"
        )


# ============================================================
# CLAP TO MUSIC
# ============================================================

def clap_to_music():

    # CHANGE THIS TO YOUR ACTUAL MUSIC FOLDER
    music_folder = (r"C:\Nova\Nova_Data\Music"
                    )
    while True:

        tt = None

        try:

            # ------------------------------------------------
            # Create microphone detector
            # ------------------------------------------------

            tt = TapTester()

            # ------------------------------------------------
            # Calibrate microphone
            # ------------------------------------------------

            threshold = calibrate_microphone(
                tt
            )
            clap_count = 0

            last_clap_time = 0

            # ------------------------------------------------
            # LISTEN FOR CLAPS
            # ------------------------------------------------

            while True:

                detected, volume = tt.listen(
                    threshold
                )

                if not detected:

                    continue

                current_time = time.time()

                # ------------------------------------------------
                # Check time between claps
                # ------------------------------------------------

                if clap_count > 0:

                    interval = (
                        current_time -
                        last_clap_time
                    )

                    # Too fast = probably same sound
                    if interval < 0.25:

                        continue

                    # Too slow = start again
                    if interval > 1.00:

                        clap_count = 0

                # ------------------------------------------------
                # Accept clap
                # ------------------------------------------------

                clap_count += 1

                last_clap_time = current_time

                """print()

                print(
                    f"👏 Clap detected! "
                    f"Volume: {volume:.5f}"
                     "---Claps: "
                    f"{clap_count}/{REQUIRED_CLAPS}"
                )

                print(

                )"""

                # ------------------------------------------------
                # REQUIRED CLAPS REACHED
                # ------------------------------------------------

                if clap_count >= REQUIRED_CLAPS:

                    """print()
                    print(
                        "🎉 Two claps detected!"
                    )

                    print(
                        "🎵 Playing random music..."
                    )"""

                    # Reset clap counter
                    clap_count = 0

                    last_clap_time = 0

                    # ------------------------------------------------
                    # Play music
                    # ------------------------------------------------

                    play_random_music(
                        music_folder
                    )

                    # ------------------------------------------------
                    # Reset detector state.
                    #
                    # This prevents the end of the previous
                    # clap from immediately triggering again.
                    # ------------------------------------------------

                    tt.in_sound_event = True
                    tt.quiet_start = None

        except KeyboardInterrupt:

            break

        except Exception as e:

            print()
            print(
                f"Error: {e}"
            )

            break

        finally:

            if tt is not None:

                tt.stop()


# ============================================================
# TEST
# ============================================================
""" 
if __name__ == "__main__":

    clap_to_music()
"""
