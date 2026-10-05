# ============================================================
# NOVA MAIN FUNCTION INTEGRATION
# ============================================================

from Functions.Check_Internet_Speed.check_speed import *
from Functions.Check_Online_Offline_Status.check_online_ofline_status import *
from Functions.Check_Temp_Wether.check_temp import *
from Functions.Clock.clock import *
from Functions.Find_My_Ip.find_my_id import *
from Functions.Clap_Detection.clap_with_music import *
from Functions.Offline_Voice.speak2 import *


# ============================================================
# NOVA FUNCTION COMMANDS
# ============================================================

def function_cmd(text):

    if not text:
        return False

    text = text.lower().strip()


    # =========================================================
    # INTERNET SPEED
    # =========================================================

    if (
        "check internet speed" in text
        or "check speed test" in text
        or "speed test" in text
        or "check the internet speed" in text

    ):

        if not get_network_status():

            fspeak(
                "I am offline right now, "
                "so I cannot check your internet speed."
            )

            return True


        check_internet_speed()

        return True


    # =========================================================
    # ONLINE / OFFLINE STATUS
    # =========================================================

    elif (
        "are you there" in text
        or "are you online" in text
        or "check your status" in text
        or "are you connected" in text
    ):

        status = internet_status()

        if status:

            if get_network_status():

                speak(
                    status
                )

            else:

                fspeak(
                    status
                )

        return True


    # =========================================================
    # TEMPERATURE
    # =========================================================

    elif (
        "check temperature" in text
        or "temperature" in text
    ):

        if not get_network_status():

            fspeak(
                "I am offline right now, "
                "so I cannot check the temperature."
            )

            return True


        city = text


        city = city.replace(
            "check the temperature of",
            ""
        ).strip()


        city = city.replace(
            "check temperature of",
            ""
        ).strip()


        city = city.replace(
            "check the temperature in",
            ""
        ).strip()


        city = city.replace(
            "check temperature in",
            ""
        ).strip()


        city = city.replace(
            "temperature of",
            ""
        ).strip()


        city = city.replace(
            "temperature in",
            ""
        ).strip()


        if city:

            check_temperature(
                city
            )

        return True


    # =========================================================
    # TIME
    # =========================================================

    elif (
        "check what's time it is" in text
        or "what's time" in text
        or "what time is it" in text
        or "check current time" in text
    ):

        what_is_the_time()

        return True


    # =========================================================
    # IP ADDRESS
    # =========================================================

    elif (
        "find my ip" in text
        or "ip address" in text
    ):

        if not get_network_status():

            fspeak(
                "I am offline right now, "
                "so I cannot find your public IP address."
            )

            return True


        ip = find_my_ip()


        speak(
            "Your IP is "
            + str(ip)
        )

        return True


    # =========================================================
    # CLAP WITH MUSIC
    # =========================================================

    elif (
        "clap with music system" in text
        or "start music with clap" in text
    ):

        speak(
            "Okay, now starting."
        )


        clap_to_music()


        return True


    # =========================================================
    # NO MATCH
    # =========================================================

    else:

        return False