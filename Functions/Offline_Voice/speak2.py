import pyttsx3
import random
import threading
import time

try:
    from textblob import TextBlob
except ImportError:
    TextBlob = None


# ============================================================
# NOVA VOICE SETTINGS
# ============================================================

# Change this to:
#
# "Heera"
# "Ravi"
# "Zira"
# "David"
# "Mark"
# "George"
# "Hazel"
# "Susan"
#
VOICE_NAME = "Zira"


DEFAULT_RATE = 175
DEFAULT_VOLUME = 1.0


# ============================================================
# GLOBAL SETTINGS
# ============================================================

SPEAKING_MODE = "normal"

PERSONALITY = "friday"

CURRENT_EMOTION = "neutral"

_stop_requested = threading.Event()

_speak_lock = threading.Lock()


# ============================================================
# PERSONALITY SETTINGS
# ============================================================

PERSONALITIES = {

    "normal": {
        "rate": 175,
        "volume": 1.0
    },

    "friday": {
        "rate": 170,
        "volume": 1.0
    },

    "jarvis": {
        "rate": 165,
        "volume": 1.0
    },

    "friendly": {
        "rate": 180,
        "volume": 1.0
    },

    "professional": {
        "rate": 165,
        "volume": 1.0
    },

    "calm": {
        "rate": 145,
        "volume": 0.95
    },

    "energetic": {
        "rate": 195,
        "volume": 1.0
    }
}


# ============================================================
# SPEAKING MODES
# ============================================================

SPEAKING_MODES = {

    "normal": {
        "rate": 175,
        "volume": 1.0
    },

    "slow": {
        "rate": 140,
        "volume": 1.0
    },

    "fast": {
        "rate": 200,
        "volume": 1.0
    },

    "quiet": {
        "rate": 165,
        "volume": 0.65
    },

    "loud": {
        "rate": 175,
        "volume": 1.0
    }
}


# ============================================================
# EMOTION KEYWORDS
# ============================================================

EMOTION_KEYWORDS = {

    "happy": [

        "happy",
        "happiness",
        "excited",
        "exciting",
        "awesome",
        "amazing",
        "great",
        "good",
        "wonderful",
        "fantastic",
        "excellent",
        "love",
        "lovely",
        "fun",
        "yay",
        "success",
        "successful",
        "glad",
        "joy",
        "joyful",
        "smile",
        "smiling",
        "nice"

    ],


    "sad": [

        "sad",
        "sadness",
        "unhappy",
        "depressed",
        "cry",
        "crying",
        "tears",
        "hurt",
        "pain",
        "lonely",
        "alone",
        "upset",
        "heartbroken",
        "disappointed",
        "disappointment"

    ],


    "angry": [

        "angry",
        "anger",
        "mad",
        "furious",
        "annoyed",
        "annoying",
        "irritated",
        "irritating",
        "hate",
        "hated",
        "rage",
        "ridiculous",
        "stupid",
        "frustrated",
        "frustration"

    ],


    "fear": [

        "afraid",
        "fear",
        "scared",
        "scary",
        "terrified",
        "terror",
        "danger",
        "dangerous",
        "worried",
        "worry",
        "nervous",
        "anxious",
        "anxiety",
        "panic"

    ],


    "surprise": [

        "surprise",
        "surprised",
        "shocked",
        "shock",
        "wow",
        "unexpected",
        "unbelievable",
        "really",
        "seriously"

    ],


    "love": [

        "love",
        "loved",
        "loving",
        "romantic",
        "care",
        "caring",
        "beautiful",
        "dear",
        "sweet"

    ],


    "confused": [

        "confused",
        "confusing",
        "confusion",
        "unclear",
        "don't understand",
        "do not understand",
        "what",
        "why",
        "how"

    ],


    "tired": [

        "tired",
        "sleepy",
        "exhausted",
        "exhausting",
        "fatigue",
        "sleep",
        "rest",
        "busy",
        "overworked"

    ],


    "neutral": []

}


# ============================================================
# EMOTION SETTINGS
# ============================================================

EMOTION_SETTINGS = {

    "happy": {
        "rate": 185,
        "volume": 1.0
    },

    "sad": {
        "rate": 140,
        "volume": 0.85
    },

    "angry": {
        "rate": 190,
        "volume": 1.0
    },

    "fear": {
        "rate": 155,
        "volume": 0.85
    },

    "surprise": {
        "rate": 195,
        "volume": 1.0
    },

    "love": {
        "rate": 165,
        "volume": 0.95
    },

    "confused": {
        "rate": 155,
        "volume": 0.9
    },

    "tired": {
        "rate": 135,
        "volume": 0.8
    },

    "neutral": {
        "rate": 175,
        "volume": 1.0
    }

}


# ============================================================
# EMOTION PHRASES
# ============================================================

EMOTION_PHRASES = {

    "happy": [

        "I'm glad to hear that.",
        "That sounds great!",
        "Awesome!",
        "That's wonderful!"

    ],


    "sad": [

        "I'm here with you.",
        "I hope things get better.",
        "Don't worry, I'm here to help."

    ],


    "angry": [

        "I understand.",
        "Let's take it one step at a time.",
        "I'll help you with that."

    ],


    "fear": [

        "Don't worry. I'm here.",
        "Let's handle this carefully.",
        "Everything is going to be okay."

    ],


    "surprise": [

        "Wow!",
        "That's unexpected.",
        "Interesting!"

    ],


    "love": [

        "That's very sweet.",
        "I appreciate that.",
        "That's nice to hear."

    ],


    "confused": [

        "Let me help you understand.",
        "Let's work through it.",
        "I'll try to make it clearer."

    ],


    "tired": [

        "You should get some rest.",
        "Take a short break.",
        "Don't push yourself too hard."

    ],


    "neutral": []

}


# ============================================================
# INITIALIZE ENGINE
# ============================================================

def create_engine():

    engine = pyttsx3.init()

    return engine


# ============================================================
# GET ALL INSTALLED VOICES
# ============================================================

def get_available_voices():

    engine = create_engine()

    voices = engine.getProperty("voices")

    print("\n======================================")
    print("Nova Installed Windows Voices")
    print("======================================")

    for index, voice in enumerate(voices):

        print(
            f"{index}: "
            f"{voice.name} "
            f"| ID: {voice.id}"
        )

    print("======================================\n")

    engine.stop()

    return voices


# ============================================================
# FIND REQUESTED WINDOWS VOICE
# ============================================================

def find_voice(voice_name=VOICE_NAME):

    engine = create_engine()

    voices = engine.getProperty("voices")

    requested = voice_name.lower().strip()

    # --------------------------------------------------------
    # First: exact keyword search
    # --------------------------------------------------------

    for voice in voices:

        name = str(
            getattr(voice, "name", "")
        ).lower()

        voice_id = str(
            getattr(voice, "id", "")
        ).lower()

        if requested in name:

            engine.stop()

            return voice.id

        if requested in voice_id:

            engine.stop()

            return voice.id


    # --------------------------------------------------------
    # If voice was not found
    # --------------------------------------------------------

    print(
        f"[Nova] Voice '{voice_name}' was not found."
    )

    print(
        "[Nova] Using the default Windows voice."
    )

    engine.stop()

    return None


# ============================================================
# SET VOICE
# ============================================================

def set_voice(voice_name):

    global VOICE_NAME

    if not voice_name:

        return False

    VOICE_NAME = voice_name

    voice_id = find_voice(
        VOICE_NAME
    )

    if voice_id:

        print(
            f"[Nova] Voice changed to: "
            f"{VOICE_NAME}"
        )

        return True

    return False


# ============================================================
# GET CURRENT VOICE
# ============================================================

def get_voice():

    return VOICE_NAME


# ============================================================
# DETECT EMOTION USING KEYWORDS
# ============================================================

def detect_emotion(text):

    if not text:

        return "neutral"


    text = text.lower()


    scores = {}


    for emotion, keywords in EMOTION_KEYWORDS.items():

        score = 0


        for keyword in keywords:

            if keyword in text:

                score += 1


        scores[emotion] = score


    if not scores:

        return "neutral"


    best_emotion = max(
        scores,
        key=scores.get
    )


    if scores[best_emotion] == 0:

        return "neutral"


    return best_emotion


# ============================================================
# GET EMOTION USING TEXTBLOB + KEYWORDS
# ============================================================

def get_emotion(text):

    if not text:

        return "neutral"


    keyword_emotion = detect_emotion(text)


    # --------------------------------------------------------
    # Keyword emotion has priority
    # --------------------------------------------------------

    if keyword_emotion != "neutral":

        return keyword_emotion


    # --------------------------------------------------------
    # TextBlob sentiment
    # --------------------------------------------------------

    if TextBlob is not None:

        try:

            sentiment = TextBlob(
                text
            ).sentiment.polarity


            if sentiment >= 0.5:

                return "happy"


            elif sentiment <= -0.5:

                return "sad"


        except Exception as e:

            print(
                f"[Nova] TextBlob error: {e}"
            )


    return "neutral"


# ============================================================
# TRACK EMOTION PHRASES
# ============================================================

def track_emotion_phrases(text):

    global CURRENT_EMOTION

    CURRENT_EMOTION = get_emotion(text)

    return CURRENT_EMOTION


# ============================================================
# GET EMOTION PHRASE
# ============================================================

def get_emotion_phrase(emotion):

    phrases = EMOTION_PHRASES.get(
        emotion,
        []
    )

    if not phrases:

        return ""


    return random.choice(
        phrases
    )


# ============================================================
# SET PERSONALITY
# ============================================================

def set_personality(name):

    global PERSONALITY

    if not name:

        return False


    name = name.lower().strip()


    if name not in PERSONALITIES:

        print(
            f"[Nova] Unknown personality: "
            f"{name}"
        )

        return False


    PERSONALITY = name


    print(
        f"[Nova] Personality: "
        f"{PERSONALITY}"
    )


    return True


# ============================================================
# GET PERSONALITY
# ============================================================

def get_personality():

    return PERSONALITY


# ============================================================
# SET SPEAKING MODE
# ============================================================

def set_speaking_mode(mode):

    global SPEAKING_MODE

    if not mode:

        return False


    mode = mode.lower().strip()


    if mode not in SPEAKING_MODES:

        print(
            f"[Nova] Unknown speaking mode: "
            f"{mode}"
        )

        return False


    SPEAKING_MODE = mode


    print(
        f"[Nova] Speaking mode: "
        f"{SPEAKING_MODE}"
    )


    return True


# ============================================================
# GET SPEAKING MODE
# ============================================================

def get_speaking_mode():

    return SPEAKING_MODE


# ============================================================
# CALCULATE SPEECH SETTINGS
# ============================================================

def get_speech_settings(emotion):

    personality_settings = PERSONALITIES.get(
        PERSONALITY,
        PERSONALITIES["normal"]
    )


    mode_settings = SPEAKING_MODES.get(
        SPEAKING_MODE,
        SPEAKING_MODES["normal"]
    )


    emotion_settings = EMOTION_SETTINGS.get(
        emotion,
        EMOTION_SETTINGS["neutral"]
    )


    # --------------------------------------------------------
    # Personality
    # --------------------------------------------------------

    rate = personality_settings["rate"]

    volume = personality_settings["volume"]


    # --------------------------------------------------------
    # Emotion modifies personality
    # --------------------------------------------------------

    emotion_rate = emotion_settings["rate"]
    emotion_volume = emotion_settings["volume"]


    rate = int(
        (rate + emotion_rate) / 2
    )


    volume = (
        volume + emotion_volume
    ) / 2


    # --------------------------------------------------------
    # Speaking mode
    # --------------------------------------------------------

    mode_rate = mode_settings["rate"]
    mode_volume = mode_settings["volume"]


    rate = int(
        (rate + mode_rate) / 2
    )


    volume = (
        volume + mode_volume
    ) / 2


    # --------------------------------------------------------
    # Keep values safe
    # --------------------------------------------------------

    rate = max(
        80,
        min(rate, 300)
    )


    volume = max(
        0.0,
        min(volume, 1.0)
    )


    return rate, volume


# ============================================================
# PRINT ANIMATED MESSAGE
# ============================================================

def print_animated_message(
        text,
        delay=0.02
):

    if not text:

        return


    print(
        "NOVA: ",
        end="",
        flush=True
    )


    for character in text:

        print(
            character,
            end="",
            flush=True
        )

        time.sleep(delay)


    print()


# ============================================================
# APPLY VOICE TO ENGINE
# ============================================================

def apply_voice(
        engine,
        voice_name=VOICE_NAME
):

    voice_id = find_voice(
        voice_name
    )


    if voice_id:

        try:

            engine.setProperty(
                "voice",
                voice_id
            )

            return True

        except Exception as e:

            print(
                f"[Nova] Could not set voice: "
                f"{e}"
            )


    return False


# ============================================================
# SPEAK BASIC
# ============================================================

def speakbasic(text):

    if not text:

        return False


    text = str(text).strip()


    if not text:

        return False


    with _speak_lock:

        _stop_requested.clear()


        # ----------------------------------------------------
        # Detect emotion
        # ----------------------------------------------------

        emotion = get_emotion(
            text
        )


        track_emotion_phrases(
            text
        )


        # ----------------------------------------------------
        # Display text
        # ----------------------------------------------------

        print_animated_message(
            text
        )


        # ----------------------------------------------------
        # Create engine
        # ----------------------------------------------------

        engine = None


        try:

            engine = create_engine()


            # ------------------------------------------------
            # Apply Windows voice
            # ------------------------------------------------

            apply_voice(
                engine,
                VOICE_NAME
            )


            # ------------------------------------------------
            # Speech settings
            # ------------------------------------------------

            rate, volume = get_speech_settings(
                emotion
            )


            engine.setProperty(
                "rate",
                rate
            )


            engine.setProperty(
                "volume",
                volume
            )


            # ------------------------------------------------
            # Speak
            # ------------------------------------------------

            engine.say(
                text
            )


            engine.runAndWait()


            return True


        except Exception as e:

            print(
                f"[Nova] Speech error: {e}"
            )

            return False


        finally:

            if engine:

                try:

                    engine.stop()

                except Exception:

                    pass


# ============================================================
# F-SPEAK
# ============================================================

def fspeak(text):

    return speakbasic(
        text
    )


# ============================================================
# STOP SPEAKING
# ============================================================

def stop_speaking():

    _stop_requested.set()


    try:

        engine = create_engine()

        engine.stop()

        engine = None

        return True

    except Exception as e:

        print(
            f"[Nova] Stop speech error: {e}"
        )

        return False


# ============================================================
# LIST VOICES
# ============================================================

def list_voices():

    return get_available_voices()


# ============================================================
# TEST CURRENT VOICE
# ============================================================

def test_voice():

    message = (
        f"Hello. I am Nova. "
        f"I am currently using the "
        f"{VOICE_NAME} voice."
    )


    return speakbasic(
        message
    )

"""
# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("======================================")
    print("        NOVA SPEAK2 VOICE SYSTEM")
    print("======================================")
    print()
    print(
        f"Selected voice: {VOICE_NAME}"
    )
    print(
        f"Personality: {PERSONALITY}"
    )
    print(
        f"Speaking mode: {SPEAKING_MODE}"
    )
    print()


    # --------------------------------------------------------
    # Show installed voices
    # --------------------------------------------------------

    voices = get_available_voices()


    # --------------------------------------------------------
    # Test selected voice
    # --------------------------------------------------------

    test_voice()
"""