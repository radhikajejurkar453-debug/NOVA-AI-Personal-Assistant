# ============================================================
# NOVA LISTENING SYSTEM
# ============================================================
#
# FEATURES
# ------------------------------------------------------------
# Online speech recognition using Google
# Offline speech recognition using Vosk
# Same captured AudioData used by Google and Vosk
# Audio energy filtering
# Wake-word listening
# Network status detection
# UI status / command / network events
# Marathi speech translation support
# EXIT COMMAND support
#
# RECOGNITION FLOW
# ------------------------------------------------------------
# Microphone
#      ↓
# Capture AudioData
#      ↓
# Check audio energy
#      ↓
# ONLINE  → Google Speech Recognition
#      ↓
# Google fails
#      ↓
# Vosk Offline Recognition
#
# OFFLINE → Vosk Offline Recognition
#
# ============================================================


import json
import socket
import audioop

import speech_recognition as sr

from vosk import (
    Model,
    KaldiRecognizer
)


# ============================================================
# PATHS
# ============================================================

VOSK_MODEL_PATH = (
    r"C:\Nova\Nova_Data\Voice_Models"
    r"\vosk-model-small-en-us-0.15"
)


# ============================================================
# SETTINGS
# ============================================================

AMBIENT_NOISE_DURATION = 0.8

PAUSE_THRESHOLD = 0.8

NON_SPEAKING_DURATION = 0.3

LISTEN_TIMEOUT = 5.0

PHRASE_TIME_LIMIT = 12.0


# ============================================================
# AUDIO ENERGY SETTINGS
# ============================================================

# Minimum RMS value considered to contain useful sound.

MIN_AUDIO_RMS = 180


# Minimum amount of PCM audio data.

MIN_AUDIO_BYTES = 3200


# ============================================================
# GLOBALS
# ============================================================

_vosk_model = None

_last_network_status = None


# ============================================================
# EXIT COMMANDS
# ============================================================

EXIT_COMMANDS = [

    # --------------------------------------------------------
    # BASIC SHUTDOWN
    # --------------------------------------------------------

    "shutdown",
    "shut down",
    "close nova",
    "close nova assistant",
    "exit nova",
    "quit nova",
    "stop nova",
    "terminate nova",

    # --------------------------------------------------------
    # CLOSE / EXIT
    # --------------------------------------------------------

    "exit",
    "quit",
    "close",
    "stop",
    "terminate",

    # --------------------------------------------------------
    # NATURAL COMMANDS
    # --------------------------------------------------------

    "nova shutdown",
    "nova shut down",
    "nova close",
    "nova exit",
    "nova quit",
    "nova stop",

    # --------------------------------------------------------
    # POLITE / NATURAL SPEECH
    # --------------------------------------------------------

    "you can stop",
    "you can shut down",
    "you can close",
    "stop now",
    "shutdown now",
    "shut down now",
    "close now",
    "exit now",

    # --------------------------------------------------------
    # USER'S EXISTING PHRASE
    # --------------------------------------------------------

    "close nova",
]

# ============================================================
# UI BRIDGE
# ============================================================

def ui_status(
    status
):

    try:

        from Interface.nova_ui_bridge import (
            emit_status
        )

        emit_status(
            status
        )

    except Exception:

        pass


# ============================================================

def ui_network_status(
    status
):

    try:

        from Interface.nova_ui_bridge import (
            emit_network_status
        )

        emit_network_status(
            status
        )

    except Exception:

        pass


# ============================================================

def ui_command(
    command
):

    try:

        from Interface.nova_ui_bridge import (
            emit_command
        )

        emit_command(
            command
        )

    except Exception:

        pass


# ============================================================
# NETWORK CHECK
# ============================================================

def check_internet():

    """
    Checks whether Nova currently has internet access.

    Uses a simple TCP connection instead of opening a browser.
    """

    hosts = [

        (
            "www.google.com",
            443
        ),

        (
            "www.microsoft.com",
            443
        ),

        (
            "www.cloudflare.com",
            443
        )

    ]

    for host, port in hosts:

        try:

            socket.create_connection(
                (
                    host,
                    port
                ),
                timeout=1.5
            )

            return True

        except Exception:

            continue

    return False


# ============================================================
# UPDATE NETWORK STATUS
# ============================================================

def update_network_status():

    """
    Checks internet availability and sends an event
    to the Nova UI only when the status changes.
    """

    global _last_network_status

    online = check_internet()

    status = (
        "ONLINE"
        if online
        else "OFFLINE"
    )

    if status != _last_network_status:

        _last_network_status = status

        ui_network_status(
            status
        )

        if status == "ONLINE":

            print(
                "🌐 NOVA: ONLINE"
            )

        else:

            print(
                "📴 NOVA: OFFLINE"
            )

    return online


# ============================================================
# AUDIO ENERGY CHECK
# ============================================================

def has_speech_energy(
    audio
):

    """
    Checks whether the captured AudioData contains
    enough acoustic energy to be treated as speech.

    IMPORTANT:
    --------------------------------------------------------
    The RMS value is only a diagnostic/filtering value.

    Google and Vosk receive the original AudioData object.
    """

    try:

        # ----------------------------------------------------
        # Get raw PCM audio
        # ----------------------------------------------------

        audio_data = (
            audio.get_raw_data(
                convert_rate=16000,
                convert_width=2
            )
        )

        # ----------------------------------------------------
        # Reject extremely small audio
        # ----------------------------------------------------

        if len(audio_data) < MIN_AUDIO_BYTES:

            print(
                "[NOVA] Audio too small."
            )

            return False

        # ----------------------------------------------------
        # Calculate RMS energy
        # ----------------------------------------------------

        rms = audioop.rms(
            audio_data,
            2
        )

        print(
            f"[NOVA] Audio energy: {rms}"
        )

        # ----------------------------------------------------
        # Reject background noise / silence
        # ----------------------------------------------------

        if rms < MIN_AUDIO_RMS:

            print(
                "[NOVA] Background noise/silence detected. "
                "Ignoring."
            )

            return False

        return True

    except Exception as e:

        print(
            "[NOVA] Audio energy check error:",
            e
        )

        # If the energy check itself fails,
        # allow the recognizer to try.

        return True


# ============================================================
# LOAD VOSK MODEL
# ============================================================

def load_vosk_model():

    global _vosk_model

    if _vosk_model is not None:

        return _vosk_model

    print(
        "[NOVA] Loading offline Vosk model..."
    )

    try:

        _vosk_model = Model(
            VOSK_MODEL_PATH
        )

        print(
            "[NOVA] Offline voice model loaded."
        )

        return _vosk_model

    except Exception as e:

        print(
            "[NOVA] Vosk model loading error:",
            e
        )

        _vosk_model = None

        return None


# ============================================================
# ONLINE GOOGLE RECOGNITION
# ============================================================

def recognize_speech_online(
    audio
):

    """
    Recognizes the SAME captured AudioData using
    Google's online speech recognition.

    The audio energy value is NOT sent to Google.
    The actual AudioData object is sent.
    """

    try:

        print(
            "[NOVA] Using ONLINE Google speech recognition..."
        )

        # ----------------------------------------------------
        # IMPORTANT
        # ----------------------------------------------------
        # This is the SAME audio object captured by
        # recognizer.listen().
        #
        # We do NOT record the microphone again.
        # ----------------------------------------------------

        text = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        text = (
            text
            .strip()
            .lower()
        )

        if text:

            print(
                "[NOVA] Google recognized:",
                text
            )

            return text

        return None

    except sr.UnknownValueError:

        print(
            "[NOVA] Google could not recognize speech."
        )

        return None

    except sr.RequestError as e:

        print(
            "[NOVA] Google speech service error:",
            e
        )

        return None

    except Exception as e:

        print(
            "[NOVA] Online recognition error:",
            e
        )

        return None


# ============================================================
# OFFLINE VOSK RECOGNITION
# ============================================================

def recognize_speech_offline(
    audio
):

    """
    Recognizes the SAME captured AudioData using Vosk.
    """

    try:

        print(
            "[NOVA] Using OFFLINE speech recognition..."
        )

        # ----------------------------------------------------
        # Check audio energy
        # ----------------------------------------------------

        if not has_speech_energy(
            audio
        ):

            return None

        # ----------------------------------------------------
        # Load Vosk
        # ----------------------------------------------------

        model = load_vosk_model()

        if model is None:

            print(
                "[NOVA] Vosk model unavailable."
            )

            return None

        # ----------------------------------------------------
        # Convert SAME AudioData to PCM
        # ----------------------------------------------------

        audio_data = (
            audio.get_raw_data(
                convert_rate=16000,
                convert_width=2
            )
        )

        # ----------------------------------------------------
        # Create recognizer
        # ----------------------------------------------------

        recognizer_vosk = (
            KaldiRecognizer(
                model,
                16000
            )
        )

        # ----------------------------------------------------
        # Send audio to Vosk
        # ----------------------------------------------------

        recognizer_vosk.AcceptWaveform(
            audio_data
        )

        result = (
            recognizer_vosk.FinalResult()
        )

        # ----------------------------------------------------
        # Read JSON result
        # ----------------------------------------------------

        data = json.loads(
            result
        )

        text = (
            data
            .get(
                "text",
                ""
            )
            .strip()
            .lower()
        )

        if text:

            print(
                "[NOVA] Vosk recognized:",
                text
            )

            return text

        print(
            "[NOVA] Vosk could not recognize speech."
        )

        return None

    except Exception as e:

        print(
            "[NOVA] Offline recognition error:",
            e
        )

        return None


# ============================================================
# MAIN SPEECH RECOGNITION
# ============================================================

def recognize_speech(
    audio,
    online
):

    """
    Uses the same captured AudioData.

    ONLINE:
        Google first
        Vosk fallback

    OFFLINE:
        Vosk directly
    """

    # ========================================================
    # ONLINE
    # ========================================================

    if online:

        text = (
            recognize_speech_online(
                audio
            )
        )

        if text:

            return text

        print(
            "[NOVA] Online recognition failed."
        )

        print(
            "[NOVA] Falling back to Vosk..."
        )

    # ========================================================
    # OFFLINE / FALLBACK
    # ========================================================

    return (
        recognize_speech_offline(
            audio
        )
    )


# ============================================================
# GLOBAL SPEECH RECOGNIZER
# ============================================================

recognizer = sr.Recognizer()

recognizer.operation_timeout = 5

recognizer.dynamic_energy_threshold = True

recognizer.pause_threshold = (
    PAUSE_THRESHOLD
)

recognizer.non_speaking_duration = (
    NON_SPEAKING_DURATION
)

recognizer.phrase_threshold = 0.3


# ============================================================
# LISTEN
# ============================================================

def listen(
    recognizer_instance=None
):

    """
    Main Nova listening function.

    Captures the microphone ONCE.

    The captured AudioData is then used by:
        Google OR Vosk

    There is no second microphone recording.
    """

    if recognizer_instance is None:

        recognizer_instance = (
            recognizer
        )

    # --------------------------------------------------------
    # Update network status
    # --------------------------------------------------------

    online = (
        update_network_status()
    )

    # --------------------------------------------------------
    # Microphone
    # --------------------------------------------------------

    try:

        with sr.Microphone() as source:

            print(
                "[NOVA] Calibrating microphone..."
            )

            recognizer_instance.adjust_for_ambient_noise(
                source,
                duration=AMBIENT_NOISE_DURATION
            )

            # ------------------------------------------------
            # Keep minimum energy threshold reasonable
            # ------------------------------------------------

            if (
                recognizer_instance.energy_threshold
                < 300
            ):

                recognizer_instance.energy_threshold = 300

            print(
                "[NOVA] Microphone ready."
            )

            print(
                "[NOVA] Energy threshold:",
                int(
                    recognizer_instance.energy_threshold
                )
            )

            ui_status(
                "LISTENING"
            )

            # ------------------------------------------------
            # Listen
            # ------------------------------------------------

            try:

                audio = (
                    recognizer_instance.listen(
                        source,
                        timeout=LISTEN_TIMEOUT,
                        phrase_time_limit=PHRASE_TIME_LIMIT
                    )
                )

            except sr.WaitTimeoutError:

                ui_status(
                    "SLEEPING"
                )

                return ""

            # ------------------------------------------------
            # IMPORTANT AUDIO CHECK
            # ------------------------------------------------
            #
            # The SAME audio object is retained.
            #
            # We do not record another sample for Google
            # or Vosk.
            # ------------------------------------------------

            if not has_speech_energy(
                audio
            ):

                ui_status(
                    "SLEEPING"
                )

                return ""

            # ------------------------------------------------
            # Thinking
            # ------------------------------------------------

            ui_status(
                "THINKING"
            )

            # ------------------------------------------------
            # Recognize SAME audio
            # ------------------------------------------------

            text = recognize_speech(
                audio,
                online
            )

            # ------------------------------------------------
            # Recognition result
            # ------------------------------------------------

            if not text:

                ui_status(
                    "SLEEPING"
                )

                return ""

            text = (
                text
                .lower()
                .strip()
            )

            # ------------------------------------------------
            # Fix common "nov" recognition
            # ------------------------------------------------

            text = text.replace(
                "nov",
                "nova"
            )

            print(
                "User :",
                text
            )

            # ------------------------------------------------
            # Send command to UI
            # ------------------------------------------------

            ui_command(
                text
            )

            # ------------------------------------------------
            # Return to active state
            # ------------------------------------------------

            ui_status(
                "ACTIVE"
            )

            return text

    except sr.WaitTimeoutError:

        ui_status(
            "SLEEPING"
        )

        return ""

    except sr.UnknownValueError:

        print(
            "[NOVA] Speech could not be understood."
        )

        ui_status(
            "SLEEPING"
        )

        return ""

    except OSError as e:

        print(
            "[NOVA] Microphone error:",
            e
        )

        ui_status(
            "ERROR"
        )

        return ""

    except Exception as e:

        print(
            "[NOVA] Listening error:",
            e
        )

        ui_status(
            "ERROR"
        )

        return ""


# ============================================================
# WAKE WORD LISTENING
# ============================================================

def hearing():

    """
    Waits for Nova's wake word.

    Example:
        "Nova"
        "Hey Nova"

    The same online/offline recognition pipeline is used.
    """

    while True:

        try:

            text = listen(
                recognizer
            )

            if not text:

                continue

            text = (
                text
                .lower()
                .strip()
            )

            # ------------------------------------------------
            # Wake words
            # ------------------------------------------------

            wake_words = [

                "nova",

                "hey nova",

                "okay nova",

                "ok nova"

            ]

            for wake_word in wake_words:

                if wake_word in text:

                    print(
                        "[NOVA] Wake word detected:",
                        text
                    )

                    ui_status(
                        "ACTIVE"
                    )

                    return text

        except KeyboardInterrupt:

            return ""

        except Exception as e:

            print(
                "[NOVA] Wake-word error:",
                e
            )

            continue


# ============================================================
# OPTIONAL MARATHI TRANSLATION
# ============================================================

def translate_marathi(
    text
):

    """
    Translates Marathi speech to English when required.

    This function is kept compatible with the previous
    listening system.

    Google Translate is only used when internet is available.
    """

    if not text:

        return ""

    try:

        from deep_translator import (
            GoogleTranslator
        )

        translated = (
            GoogleTranslator(
                source="mr",
                target="en"
            )
            .translate(
                text
            )
        )

        if translated:

            return (
                translated
                .strip()
                .lower()
            )

    except Exception as e:

        print(
            "[NOVA] Marathi translation error:",
            e
        )

    return text

"""
# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print()
    print(
        "================================================"
    )
    print(
        "          NOVA LISTENING TEST"
    )
    print(
        "================================================"
    )
    print()

    print(
        "[NOVA] Say something..."
    )

    while True:

        result = listen(
            recognizer
        )

        if result:

            print(
                "NOVA RESULT:",
                result
            )

        print()
"""