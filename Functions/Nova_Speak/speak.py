# ============================================================
# NOVA SPEAK - AUTOMATIC ONLINE / OFFLINE VOICE SWITCHING
# ============================================================
#
# ONLINE:
#   Edge TTS - en-US-JennyNeural
#
# OFFLINE:
#   Functions\Offline_Voice\speak2.py
#   Uses the selected Windows voice, currently Zira
#
# BEHAVIOR:
#   1. Try Edge TTS for every response.
#   2. If Edge TTS fails, use speak2.py.
#   3. Retry Edge TTS on the next response.
#   4. Automatically return to Edge TTS when it works.
#   5. Preserve Nova UI status and response integration.
#
# No changes required to main.py, the UI, or speak2.py.
# ============================================================

import os
import sys
import asyncio
import tempfile
import threading
import time
import warnings

warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API"
)

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# ONLINE VOICE SETTINGS
# ============================================================

VOICE = "en-US-JennyNeural"

EDGE_TTS_TIMEOUT = 25
EDGE_CONNECT_TIMEOUT = 5
EDGE_RECEIVE_TIMEOUT = 10


# ============================================================
# SPEECH CONTROL
# ============================================================

_speech_lock = threading.Lock()


# ============================================================
# LOAD OFFLINE VOICE SYSTEM
# ============================================================

try:
    from Functions.Offline_Voice import speak2 as offline_voice

    if not callable(getattr(offline_voice, "speakbasic", None)):
        raise AttributeError(
            "speak2.py does not provide speakbasic(text)."
        )

    print("[NOVA] Offline speak2 voice system loaded.")

except Exception as e:
    offline_voice = None

    print(
        "[NOVA] Could not load speak2.py:",
        repr(e)
    )


# ============================================================
# UI BRIDGE
# ============================================================

def ui_status(status):
    try:
        from Interface.nova_ui_bridge import emit_status
        emit_status(status)

    except Exception as e:
        print("[UI STATUS ERROR]:", e)


def ui_response(text):
    try:
        from Interface.nova_ui_bridge import emit_response
        emit_response(text)

    except Exception as e:
        print("[UI RESPONSE ERROR]:", e)


# ============================================================
# EDGE TTS
# ============================================================

def speak_edge(text):
    file_path = None

    try:
        import edge_tts

        # ----------------------------------------------------
        # CREATE A UNIQUE AUDIO FILE
        # ----------------------------------------------------

        file_descriptor, file_path = tempfile.mkstemp(
            prefix="Nova_speech_",
            suffix=".mp3"
        )

        os.close(file_descriptor)

        # ----------------------------------------------------
        # GENERATE NEURAL SPEECH
        # ----------------------------------------------------

        async def generate():
            communicate = edge_tts.Communicate(
                text,
                VOICE,
                connect_timeout=EDGE_CONNECT_TIMEOUT,
                receive_timeout=EDGE_RECEIVE_TIMEOUT
            )

            await communicate.save(file_path)

        print("[NOVA] Connecting to Edge TTS...")

        asyncio.run(
            asyncio.wait_for(
                generate(),
                timeout=EDGE_TTS_TIMEOUT
            )
        )

        # ----------------------------------------------------
        # CHECK GENERATED AUDIO
        # ----------------------------------------------------

        if not os.path.isfile(file_path):
            print("[NOVA] Edge TTS did not create an audio file.")
            return False

        if os.path.getsize(file_path) == 0:
            print("[NOVA] Edge TTS returned an empty audio file.")
            return False

        # ----------------------------------------------------
        # PLAY NEURAL VOICE
        # ----------------------------------------------------

        print("[NOVA] Playing neural voice:", VOICE)

        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        playback_timeout = max(
            30,
            (len(text.split()) / 2.5) + 20
        )

        playback_started = time.monotonic()
        clock = pygame.time.Clock()

        while pygame.mixer.music.get_busy():
            if (
                time.monotonic() - playback_started
                > playback_timeout
            ):
                print("[NOVA] Edge TTS playback timed out.")
                return False

            clock.tick(10)

        return True

    except asyncio.TimeoutError:
        print("[NOVA] Edge TTS request timed out.")
        return False

    except Exception as e:
        print("[NOVA] Edge TTS error:", repr(e))
        return False

    finally:
        # ----------------------------------------------------
        # CLEAN UP AUDIO
        # ----------------------------------------------------

        try:
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
                pygame.mixer.quit()

        except Exception as e:
            print("[NOVA] Audio cleanup warning:", e)

        # ----------------------------------------------------
        # DELETE TEMPORARY FILE
        # ----------------------------------------------------

        if file_path:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)

            except OSError as e:
                print("[NOVA] Temporary file cleanup warning:", e)


# ============================================================
# OFFLINE FALLBACK - USE speak2.py
# ============================================================

def speak_offline(text):
    if offline_voice is None:
        print("[NOVA] Offline speak2 voice system is unavailable.")
        return False

    try:
        print("[NOVA] Switching to offline Windows voice.")
        print("[NOVA] Offline voice:", offline_voice.get_voice())

        # Uses your existing speak2.py features:
        # - Selected Windows voice (Zira in your pasted code)
        # - Personality settings
        # - Speaking modes
        # - Emotion detection
        # - Emotion-based speech rate and volume

        result = offline_voice.speakbasic(text)

        if result:
            print("[NOVA] Offline speech successful.")
            return True

        print("[NOVA] Offline speech returned failure.")
        return False

    except Exception as e:
        print("[NOVA] Offline speech error:", repr(e))
        return False


# ============================================================
# MAIN NOVA SPEAK FUNCTION
# ============================================================

def speak(text):
    if text is None:
        return False

    text = str(text).strip()

    if not text:
        return False

    # Prevent overlapping online/offline speech requests.
    with _speech_lock:
        try:
            print("NOVA:", text)

            # Display the response once in the Nova UI.
            ui_response(text)
            ui_status("SPEAKING")

            # ------------------------------------------------
            # ALWAYS TRY EDGE TTS FIRST
            # ------------------------------------------------
            #
            # We deliberately retry Edge TTS for every response.
            # A previous DNS or network failure does not disable
            # the neural voice for future responses.
            #
            # ------------------------------------------------

            print("[NOVA] Trying Edge TTS...")

            if speak_edge(text):
                print("[NOVA] Edge TTS successful.")
                ui_status("ACTIVE")
                return True

            # ------------------------------------------------
            # AUTOMATIC OFFLINE FALLBACK
            # ------------------------------------------------

            print(
                "[NOVA] Edge TTS unavailable. "
                "Using speak2.py offline voice."
            )

            if speak_offline(text):
                ui_status("ACTIVE")
                return True

            # ------------------------------------------------
            # BOTH SYSTEMS FAILED
            # ------------------------------------------------

            print("[NOVA] ERROR: Online and offline speech failed.")
            ui_status("ERROR")
            return False

        except Exception as e:
            print("[NOVA] Unexpected speech error:", repr(e))
            ui_status("ERROR")
            return False


# ============================================================
# TEST
# ============================================================
"""
if __name__ == "__main__":
    print()
    print("=" * 60)
    print("NOVA AUTOMATIC VOICE SWITCHING TEST")
    print("=" * 60)

    speak(
        "Hello. I am Nova. "
        "I will use my neural voice when available "
        "and switch to my offline voice if necessary."
    )
"""