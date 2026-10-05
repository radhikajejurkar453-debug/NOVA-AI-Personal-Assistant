import pyaudio
import struct
import math
import time


# ============================================================
# SETTINGS
# ============================================================

REQUIRED_CLAPS = 2

# Minimum time between two separate claps
MIN_CLAP_INTERVAL = 0.25

# Maximum time allowed between two claps
MAX_CLAP_INTERVAL = 1.00

# Time the microphone must remain quiet before
# another clap can be detected
QUIET_RESET_TIME = 0.15

# Minimum volume required to consider a sound
# as a possible clap
MIN_CLAP_THRESHOLD = 0.30


# ============================================================
# AUDIO SETTINGS
# ============================================================

FORMAT = pyaudio.paInt16

SHORT_NORMALIZE = 1.0 / 32768.0

# We use ONE channel even if the microphone has 4 channels.
CHANNELS = 1

INPUT_BLOCK_TIME = 0.01

INPUT_FRAMES_PER_BLOCK = int(
    44100 * INPUT_BLOCK_TIME
)


# ============================================================
# CLAP DETECTOR STATE
# ============================================================

class TapTester:

    def __init__(self):

        self.pa = pyaudio.PyAudio()

        self.stream = self.open_mic_stream()

        # ----------------------------------------------------
        # Detector state
        # ----------------------------------------------------

        self.in_sound_event = False

        self.quiet_start = None

        # Time of the last accepted clap
        self.last_detection_time = 0

    # ========================================================
    # STOP MICROPHONE
    # ========================================================

    def stop(self):

        try:
            self.stream.stop_stream()
            self.stream.close()
        finally:
            self.pa.terminate()

    # ========================================================
    # FIND DEFAULT MICROPHONE
    # ========================================================

    def find_input_device(self):

        device = self.pa.get_default_input_device_info()

        device_index = int(
            device["index"]
        )
        return device_index
    """"
        print("----------------------------------------")
        print("DEFAULT INPUT DEVICE")
        print("----------------------------------------")

        print(
            "Device index:",
            device_index
        )

        print(
            "Name:",
            device["name"]
        )
    """


    # ========================================================
    # OPEN MICROPHONE
    # ========================================================

    def open_mic_stream(self):

        device_index = self.find_input_device()

        device_info = self.pa.get_device_info_by_index(
            device_index
        )

        sample_rate = int(
            device_info["defaultSampleRate"]
        )

        stream = self.pa.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=sample_rate,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=INPUT_FRAMES_PER_BLOCK
        )
        return stream
    """
        print("----------------------------------------")
        print("MICROPHONE")
        print("----------------------------------------")

        print(
            "Device:",
            device_index
        )

        print(
            "Name:",
            device_info["name"]
        )

        print(
            "Available channels:",
            device_info["maxInputChannels"]
        )

        print(
            "Sample rate:",
            sample_rate
        )

        print("----------------------------------------")
    """

        # ----------------------------------------------------
        # Use ONE channel.
        # This avoids multi-channel RMS problems.
        # ----------------------------------------------------



    # ========================================================
    # CALCULATE RMS
    # ========================================================

    @staticmethod
    def get_rms(block):

        count = len(block) // 2

        if count == 0:
            return 0.0

        samples = struct.unpack(
            f"{count}h",
            block
        )

        total = 0.0

        for sample in samples:

            value = (
                sample *
                SHORT_NORMALIZE
            )

            total += value * value

        return math.sqrt(
            total / count
        )

    # ========================================================
    # READ MICROPHONE VOLUME
    # ========================================================

    def read_volume(self):

        try:

            block = self.stream.read(
                INPUT_FRAMES_PER_BLOCK,
                exception_on_overflow=False
            )

        except IOError:

            return 0.0

        return self.get_rms(block)

    # ========================================================
    # LISTEN FOR ONE CLAP
    # ========================================================

    def listen(self, threshold):

        volume = self.read_volume()

        '''print(
            f"\rVolume: {volume:.5f}",
            end="",
            flush=True
        )'''

        current_time = time.time()

        # ====================================================
        # STATE 1:
        # WE ARE ALREADY INSIDE A LOUD SOUND
        # ====================================================

        if self.in_sound_event:

            # ------------------------------------------------
            # Sound is still loud.
            #
            # IMPORTANT:
            # Do NOT detect it again.
            # ------------------------------------------------

            if volume >= threshold:

                self.quiet_start = None

                return False, volume

            # ------------------------------------------------
            # Sound has become quiet.
            # ------------------------------------------------

            else:

                if self.quiet_start is None:

                    self.quiet_start = current_time

                    return False, volume

                quiet_time = (
                    current_time -
                    self.quiet_start
                )

                # ------------------------------------------------
                # The sound must remain quiet for a short time
                # before another clap can be accepted.
                # ------------------------------------------------

                if quiet_time >= QUIET_RESET_TIME:

                    self.in_sound_event = False

                    self.quiet_start = None

                return False, volume

        # ====================================================
        # STATE 2:
        # WAITING FOR A NEW SOUND
        # ====================================================

        if volume >= threshold:

            # ------------------------------------------------
            # Extra protection against immediate retriggering
            # ------------------------------------------------

            if (
                current_time -
                self.last_detection_time
                < MIN_CLAP_INTERVAL
            ):

                self.in_sound_event = True

                return False, volume

            # ------------------------------------------------
            # NEW SOUND EVENT
            # ------------------------------------------------

            self.in_sound_event = True

            self.quiet_start = None

            self.last_detection_time = current_time

            return True, volume

        return False, volume


# ============================================================
# MICROPHONE CALIBRATION
# ============================================================

def calibrate_microphone(tt):

    values = []

    start_time = time.time()

    while time.time() - start_time < 3:

        volume = tt.read_volume()

        values.append(volume)

    if not values:

        return MIN_CLAP_THRESHOLD

    # --------------------------------------------------------
    # Calculate average background noise
    # --------------------------------------------------------

    background_noise = (
        sum(values) /
        len(values)
    )

    # --------------------------------------------------------
    # Calculate threshold from background noise
    # --------------------------------------------------------

    calculated_threshold = (
        background_noise * 8
    )

    # --------------------------------------------------------
    # Do not allow threshold to become too low.
    # --------------------------------------------------------

    threshold = max(
        calculated_threshold,
        MIN_CLAP_THRESHOLD
    )

    return threshold
'''
    print("----------------------------------------")

    print(
        f"Background noise: "
        f"{background_noise:.5f}"
    )

    print(
        f"Calculated threshold: "
        f"{calculated_threshold:.5f}"
    )

    print(
        f"Final clap threshold: "
        f"{threshold:.5f}"
    )

    print("----------------------------------------")'''



# ============================================================
# DOUBLE-CLAP DETECTION
# ============================================================

def clap_detect():

    tt = TapTester()

    clap_count = 0
    last_clap_time = 0

    try:

        # ----------------------------------------------------
        # Calibrate microphone
        # ----------------------------------------------------

        threshold = calibrate_microphone(tt)


        # ----------------------------------------------------
        # Main detection loop
        # ----------------------------------------------------

        while True:

            detected, volume = tt.listen(threshold)

            if not detected:
                continue

            current_time = time.time()

            # =================================================
            # CHECK TIME BETWEEN CLAPS
            # =================================================

            if clap_count > 0:

                interval = (
                    current_time - last_clap_time
                )

                # Too fast = same sound
                if interval < MIN_CLAP_INTERVAL:
                    continue

                # Too slow = start a new double-clap sequence
                if interval > MAX_CLAP_INTERVAL:
                    clap_count = 0

            # =================================================
            # ACCEPT CLAP
            # =================================================

            clap_count += 1
            last_clap_time = current_time

            # ------------------------------------------------
            # EXACT OUTPUT YOU WANT
            # ------------------------------------------------

            print()
            print(
                f"👏 Clap detected!---- "
                f"Volume: {volume:.5f} -- "
                f"Claps: {clap_count}/{REQUIRED_CLAPS}"
            )

            # =================================================
            # TWO CLAPS DETECTED
            # =================================================

            if clap_count >= REQUIRED_CLAPS:

                print()
                print(
                    "🎉 Two claps detected! --- "
                    "🚀 NOVA triggered!"
                )

                print(
                    "Listening for next two claps..."
                )

                print("----------------------------------------")

                # Reset clap sequence
                clap_count = 0
                last_clap_time = 0

                # ------------------------------------------------
                # IMPORTANT:
                # Do not immediately detect the same loud sound
                # as another clap.
                # ------------------------------------------------

                tt.in_sound_event = True
                tt.quiet_start = None

    except KeyboardInterrupt:

        print()
        print()
        print("🛑 Clap detection stopped.")

    finally:

        tt.stop()


# ============================================================
# TEST
# ============================================================
"""
if __name__ == "__main__":
    clap_detect()
"""
