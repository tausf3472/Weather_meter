import requests

def weather(city: str) -> None:
    # 1) Geocode city -> lat/lon
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo = requests.get(
        geo_url,
        params={"name": city, "count": 1, "language": "en", "format": "json"},
        timeout=10
    ).json()

    results = geo.get("results", [])
    if not results:
        print("City not found. Try a different name (e.g., 'Bokaro, Jharkhand').")
        return

    place = results[0]
    lat, lon = place["latitude"], place["longitude"]

    # 2) Get current weather
    wx_url = "https://api.open-meteo.com/v1/forecast"
    wx = requests.get(
        wx_url,
        params={
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "timezone": "auto"
        },
        timeout=10
    ).json()

    current = wx.get("current_weather")
    if not current:
        print("Could not fetch current weather right now.")
        return

    name = place.get("name", city)
    admin1 = place.get("admin1", "")
    country = place.get("country", "")
    location_str = ", ".join([x for x in [name, admin1, country] if x])

    print(f"Location: {location_str}")
    print(f"Temperature: {current['temperature']}°C")
    print(f"Wind Speed: {current['windspeed']} km/h")

city = input("Enter the Name of Any City >> ").strip()
weather(city)
