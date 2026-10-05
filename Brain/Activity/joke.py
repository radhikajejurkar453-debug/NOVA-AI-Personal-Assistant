import requests

from Functions.Nova_Speak.speak import speak


# =========================================================
# GET RANDOM JOKE
# =========================================================

def get_random_joke():

    try:

        headers = {
            "Accept": "application/json"
        }

        response = requests.get(
            "https://icanhazdadjoke.com/",
            headers=headers,
            timeout=5
        )

        response.raise_for_status()

        data = response.json()

        return data["joke"]

    except requests.RequestException as e:

        print(
            "Joke API error:",
            e
        )

        return (
            "Sorry, I could not get a joke "
            "right now."
        )

    except (KeyError, ValueError) as e:

        print(
            "Joke API data error:",
            e
        )

        return (
            "Sorry, I could not understand "
            "the joke service."
        )


# =========================================================
# JOKE COMMAND
# =========================================================

def jokes():

    # Nova immediately responds.
    speak(
        "Sure! Here's a joke."
    )

    # Get a random joke.
    joke = get_random_joke()

    # Speak the joke.
    speak(joke)

    return True


# =========================================================
# TESTING ONLY
# =========================================================

"""
jokes()
"""