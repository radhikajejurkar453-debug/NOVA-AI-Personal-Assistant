import requests

def find_my_ip():

    try:

        response = requests.get(
            "https://api64.ipify.org?format=json",
            timeout=5
        )

        response.raise_for_status()

        ip_address = response.json()

        return ip_address["ip"]

    except requests.RequestException as e:

        print("Unable to find IP address:", e)

        return None
'''
# testing only
x = find_my_ip()
print(x)'''