import requests
from Functions.Nova_Speak.speak import speak

API_KEY = "da0eb7008259ac53a4dca3cf1aba9c87"


def check_temperature(city):
    if API_KEY == "YOUR_OPENWEATHER_API_KEY":
        print("❌ API key not configured.")
        speak("Please configure the weather API key.")
        return None

    try:

        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        weather = data["weather"][0]["description"]

        message = (
            f"The temperature in {city} is "
            f"{temperature:.1f} degrees Celsius. "
            f"It feels like {feels_like:.1f} degrees. "
            f"The weather is {weather}, "
            f"with humidity at {humidity} percent."
        )

        speak(message)

        return data

    except requests.exceptions.RequestException as e:

        print("❌ Weather API error:", e)
        speak("Sorry, I could not get the weather information.")
        return None



# ============================================================
# TESTING
# ============================================================
""" 
if __name__ == "__main__":
   
check_temperature("thailand")
"""

