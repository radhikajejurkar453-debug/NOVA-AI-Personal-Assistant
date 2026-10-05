import os
import sys


from Functions.Nova_Speak.speak import speak


def _load_speedtest():

    """
    Load speedtest safely when Nova is running with pythonw.exe.

    pythonw.exe does not provide normal stdout/stderr streams.
    Older speedtest-cli versions expect stdout/stderr to exist.
    """

    if sys.stdout is None:

        sys.stdout = open(
            os.devnull,
            "w",
            encoding="utf-8",
            buffering=1
        )

    if sys.stderr is None:

        sys.stderr = open(
            os.devnull,
            "w",
            encoding="utf-8",
            buffering=1
        )

    import speedtest

    return speedtest


def get_internet_speed():

    try:

        speak(
            "Checking your internet speed. Please wait."
        )

        speedtest = _load_speedtest()

        st = speedtest.Speedtest()

        # Find the best server
        st.get_best_server()

        # Test download speed
        download_speed = st.download()

        # Test upload speed
        upload_speed = st.upload()

        # Convert bits per second to Mbps
        download_mbps = download_speed / 1_000_000
        upload_mbps = upload_speed / 1_000_000

        return download_mbps, upload_mbps

    except Exception as e:

        print(
            "Internet speed error:",
            e
        )

        return None, None


def check_internet_speed():

    download_speed, upload_speed = get_internet_speed()

    if download_speed is not None:

        speak(
            f"Your download speed is "
            f"{download_speed:.2f} Mbps "
            f"and your upload speed is "
            f"{upload_speed:.2f} Mbps."
        )

    else:

        speak(
            "Sorry, I was unable to check your internet speed."
        )


"""
# for testing only
check_internet_speed()
"""