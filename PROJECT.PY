import requests, sys
from tabulate import tabulate
from pyfiglet import Figlet
from colorama import Fore, Style, init

# Initialize colorama (important for Windows)
init(autoreset=True)

# -------------------------------
# MAIN PROGRAM
# -------------------------------

def main():
    area = input("Enter Area Name: ").strip()
    lat, lon = get_area(area)
    weather(lat, lon)


# -------------------------------
# FUNCTION 1: Get latitude & longitude
# -------------------------------

def get_area(ar):
    try:
        response = requests.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={ar}&appid=0da102f5f62e49334448cfe39a3159a8"
        )

        data = response.json()

        if not data:
            raise Exception()

    except Exception:
        sys.exit("❌ Invalid area name. Try again.")

    return data[0]["lat"], data[0]["lon"]
# -------------------------------
# FUNCTION 2: Get weather + table
# -------------------------------

def weather(lat, lon):
    try:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=e8cde7fb8c3391c297d032915416fe6c"
        )

        data = response.json()

    except Exception as e:
        sys.exit(f" Error fetching weather data: {e}")

    temp_k = data["main"]["temp"]
    temp_c = round(temp_k - 273.15, 1)

    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]

    wind_ms = data["wind"]["speed"]
    wind_kmh = round(wind_ms * 3.6, 1)

    visibility_m = data.get("visibility")
    visibility_km = f"{visibility_m/1000:.1f} km" if visibility_m else "N/A"

    description = data["weather"][0]["description"]
    location = data["name"]
    country = data["sys"]["country"]

    # Table with layman units
    f_data = {
        "Location": f"{location}, {country}",
        "Temperature": f"{temp_c} °C",
        "Humidity": f"{humidity}%",
        "Pressure": f"{pressure} hPa",
        "Wind Speed": f"{wind_kmh} km/h",
        "Visibility": visibility_km,
        "Description": description.capitalize(),
    }
    # Fancy title
    print(Figlet(font="slant").renderText("Weather Report"))

    print(tabulate(f_data.items(), headers=["PARAMETER", "VALUE"], tablefmt="grid"))

    give_advice(description)


# -------------------------------
# FUNCTION 3: Colour-coded Figlet Advice
# -------------------------------

def give_advice(desc):
    fig = Figlet(font="slant")
    desc = desc.lower()

    if "rain" in desc:
        advice = "Carry an umbrella!"
        color = Fore.BLUE

    elif "clear" in desc:
        advice = "Nice day! Wear sunglasses."
        color = Fore.YELLOW

    elif "cloud" in desc:
        advice = "It might get chilly, take a light jacket."
        color = Fore.CYAN

    elif "snow" in desc:
        advice = "Dress warmly, it's snowy outside!"
        color = Fore.WHITE

    elif "storm" in desc or "thunder" in desc:
        advice = "Stay indoors, weather is risky."
        color = Fore.RED

    elif "mist" in desc or "fog" in desc:
        advice = "Drive carefully, visibility is low."
        color = Fore.MAGENTA

    else:
        advice = "Weather looks normal. Have a good day!"

    print(color + fig.renderText("ADVICE"))
    print(color + advice)
        ascii_advice = fig.renderText(advice)
    print(color + ascii_advice + Style.RESET_ALL)


# -------------------------------
# RUN PROGRAM
# -------------------------------

if __name__ == "__main__":
    main()



