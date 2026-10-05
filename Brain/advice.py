import requests

from Functions.Nova_Speak.speak import speak


def get_random_advice():

    try:

        response = requests.get(
            "https://api.adviceslip.com/advice",
            timeout=5
        )

        response.raise_for_status()

        data = response.json()

        return data["slip"]["advice"]

    except requests.RequestException as e:

        print("Advice API error:", e)

        return "Sorry, I could not get any advice right now."

    except (KeyError, ValueError) as e:

        print("Advice API data error:", e)

        return "Sorry, I could not understand the advice service."


def advice():

    speak("Sure, here is some advice.")

    advice_text = get_random_advice()

    speak(advice_text)

    return True


# if __name__ == "__main__":
#     advice()